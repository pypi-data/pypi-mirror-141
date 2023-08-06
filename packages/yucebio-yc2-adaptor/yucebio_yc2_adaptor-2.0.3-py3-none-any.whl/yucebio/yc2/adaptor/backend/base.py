import io
import sys
import json
import os
from typing import Any
import zipfile
from importlib_metadata import pathlib
import requests

from yucebio.yc2.adaptor.util.config import Config
from yucebio.yc2.adaptor.util.input_processor import InputProcessor
from yucebio.yc2.adaptor.util.wdl_processor import WorkflowProcess, _TaskItem
from .types import BackendConfigType

PLACEHOLDER_GLOBAL_PATH = '__GLOBAL__'
PLACEHOLDER_SIMG_PATH = '__SIMG__'


class BaseAdaptor(object):

    wdl_version = 1.0
    PLATFORM = "default"
    HOST = "http://127.0.0.1:8000"
    COMMAND_PREFIX = "singularity exec -W /cromwell_root -B %s,/cromwell_root,/cromwell_inputs ~{simg}"
    SUPPORTED_RUNTIME_ATTRIBUTES = ['cpu', 'memory', 'maxRetries']

    def __init__(self, backend_config: BackendConfigType = None) -> None:
        self.backend_config = backend_config
        
        self.input_processor = None
        self.workflow_processor = None

        # 存放每个import的task信息
        self.meta = {}
        self._config = Config()

        # 用于支持添加全局runtime属性
        self.global_runtimes = {}

    @property
    def supported_runtime_attributes(self):
        return (self.backend_config.get('runtimes') or []) + (self.SUPPORTED_RUNTIME_ATTRIBUTES or [])

    def config(self, key: str = None) -> dict:
        """查询或更新配置:  cromwell api地址， 公共目录以及simg目录必须配置
        1. 查询              c = adaptor.config()
        2. 查询指定配置      c  = adaptor.config('aws')
        """
        if key:
            return self._config.get(key, {})
        return self._config.config

    @property
    def global_path(self):
        return self.backend_config.get('global_path')
    
    @property
    def simg_path(self):
        return self.backend_config.get('simg_path')

    @property
    def bind_path(self):
        """将command放到singularity中执行时，需要指定映射的目录"""
        return self.global_path + ',' + self.simg_path

    def parse_input(self, input_path: str = None):
        if isinstance(input_path, InputProcessor):
            self._input_file = input_path.filepath
            self.input_processor = input_path
            return 

        if input_path:
            self._input_file = input_path
        self.input_processor = InputProcessor(self._input_file)

    def parse_workflow(self, wdl_path: str = None, package_path: str = None):
        if wdl_path:
            self._wdl_path = wdl_path
        self.workflow_processor = WorkflowProcess(self._wdl_path, package_path=package_path)

    def parse(self, wdl_path: str=None, input_path: str=None, **kw):
        self.parse_input(input_path)
        self.parse_workflow(wdl_path, package_path=kw.get('package_path'))
        if not self.global_path:
            raise RuntimeError(f"请配置当前平台[{self.PLATFORM.lower()}(别名{self.config_alias})]的公共目录路径[global_path]")

        # @2021年8月20日 支持添加静态自定义runtime属性
        if kw.get('runtimes'):
            # 获取用户提供的需要自动添加的runtime属性
            runtime_keys = kw["runtimes"].split(',')
            # 从input_json中提取自动添加的runtime属性值
            inputs = self.input_processor.inputs
            for k in runtime_keys:
                if k not in inputs:
                    raise RuntimeError(f"请在{self.input_processor.filepath}中提供[{self.input_processor.workflow_name}.{k}]初始值")
                self.global_runtimes[k] = inputs[k]

    def convert(self):
        """遍历每个import，依次转换每个task

        Description
            1. 常规情况下，input.json无需处理，只有阿里云中涉及到动态资源时，需要添加额外的input
            2. 常规情况下，workflow无需处理，只有阿里云中涉及到动态资源时，可能需要处理call.input和workflow.input
            3. 大部分情况下需要对task的command做转换
        原理
            1. 加载json并解析
            2. 加载workflow.wdl并解析
            3. 遍历workflow.wdl的imports，依次处理每个task
            3.1 根据workflow.calls决定是否需要移除未使用的task
            3.2 阿里云根据task是否存在可变资源决定是否修改input.json和workflow
            3.3 根据平台修改command
        """
        raise NotImplementedError("method 'convert' should implemented by sub class")

    def filter_or_append_runtime_attributes(self, ti: _TaskItem):
        """移除不支持的runtime属性、并添加默认runtime属性
        """
        # 移除不支持的RUNTIME属性
        if self.supported_runtime_attributes:
            for k in dict(ti.runtime):
                if k not in self.supported_runtime_attributes:
                    print("DELETE NOT SUPPORTED RUNTIME ATTRIBUTE:", k, file=sys.stderr)
                    ti.delete_runtime(k)

        # 添加默认runtime属性
        if not self.global_runtimes:
            return
        for k,v in self.global_runtimes.items():
            ti.update_runtime(k, repr(v))

        self.filter_unused_input_attributes(ti)

    def filter_unused_input_attributes(self, ti: _TaskItem):
        """@TODO: 2021-09-07 检查task的input参数与input.json中的参数是否一致
        """

        pass

    def pp(self, obj: Any):
        print(json.dumps(obj, indent=2, default=str))

    @property
    def stream_workflow(self) -> io.BytesIO:
        return io.BytesIO(str(self.workflow_processor).encode('utf8'))
    
    @property
    def stream_input(self) -> io.BytesIO:
        context = str(self.input_processor)
        if PLACEHOLDER_GLOBAL_PATH in context:
            global_path = self.global_path
            if not global_path:
                raise RuntimeError(f"请配置global_path参数")
            context = context.replace(PLACEHOLDER_GLOBAL_PATH, global_path)
        if PLACEHOLDER_SIMG_PATH in context:
            simg_path = self.simg_path
            if not simg_path:
                raise RuntimeError(f"请配置simg_path参数")
            context = context.replace(PLACEHOLDER_SIMG_PATH, simg_path)
        return io.BytesIO(context.encode('utf8'))
    
    @property
    def stream_bundle(self) -> io.BytesIO:
        
        if not self.workflow_processor.imports:
            return None

        in_memory_file = io.BytesIO()
        z = zipfile.ZipFile(in_memory_file, 'a')

        for import_item in self.workflow_processor.imports.values():
            wdl = import_item.wdl

            # 打包导入文件到tar中
            dirname = os.path.dirname(import_item.path) + '/'
            if dirname not in z.namelist():
                # print('add path', dirname)
                zipinfo_dir = zipfile.ZipInfo(dirname)
                zipinfo_dir.compress_type = zipfile.ZIP_STORED
                zipinfo_dir.external_attr = 0o40755 << 16       # permissions drwxr-xr-x
                zipinfo_dir.external_attr |= 0x10               # MS-DOS directory flag
                z.writestr(zipinfo_dir, '')

            zipinfo = zipfile.ZipInfo(import_item.path)
            zipinfo.external_attr = 0o644 << 16                 # permissions -r-wr--r--
            
            # click.secho(f"in base zip_import_file: path[{wdl.fileWdl}] id[{id(wdl)}]", fg='green')
            z.writestr(zipinfo, str(wdl))
        z.close()
        in_memory_file.seek(0)
        return in_memory_file

    def generate_file(self, outdir = './'):
        """生成适配后的输出文件
        """
        cfg = self.backend_config
        # 任务投递shell： 
        restful_content = [
            'curl -X POST "{host}/api/workflows/v1"',
            '-H "accept: application/json" -H "Content-Type: multipart/form-data"',
            '-F "workflowSource=@{wdl}"',
            '-F "workflowInputs=@{input_json};type=application/json"'
        ]
        host = cfg.get('host', self.HOST)

        platform = "default" if not self.PLATFORM else self.PLATFORM
        output_path = pathlib.Path(outdir)/platform.lower()
        output_path.mkdir(parents=True, exist_ok=True)
        # bundle = "bundle." + platform + ".tar"

        bundle_file = self.zip_import_file(path=output_path)
        if bundle_file:
            restful_content.append('-F "workflowDependencies=@{bundle};type=application/x-zip-compressed"')

        # wdl = '/'.join([output_path, os.path.basename(self.workflow_processor.fileWdl)])
        wdl = output_path/os.path.basename(self.workflow_processor.fileWdl)
        with open(wdl, 'w', encoding='utf8') as w:
            w.write(str(self.workflow_processor))

        # input_json = '.'.join([os.path.splitext(self.input_processor.filepath)[0], platform, 'json'])
        input_json = output_path/(os.path.splitext(os.path.basename(self.input_processor.filepath))[0] + ".json")
        # input_json = '/'.join([
            # output_path, 
            # os.path.splitext(os.path.basename(self.input_processor.filepath))[0] + ".json"
        # ])
        with open(input_json, 'w', encoding='utf8') as w:
            context = str(self.input_processor)
            if PLACEHOLDER_GLOBAL_PATH in context:
                global_path = self.global_path
                if not global_path:
                    raise RuntimeError(f"请配置global_path参数")
                context = context.replace(PLACEHOLDER_GLOBAL_PATH, global_path)
            if PLACEHOLDER_SIMG_PATH in context:
                simg_path = self.simg_path
                if not simg_path:
                    raise RuntimeError(f"请配置simg_path参数")
                context = context.replace(PLACEHOLDER_SIMG_PATH, simg_path)
            w.write(context)

        print("\n", (' \\\n\t'.join(restful_content)).format(
                host=host, wdl=wdl, input_json=input_json, bundle=bundle_file
            )
        )

    def zip_import_file(self, existsZip=None, path="./"):
        """打包导入文件
        """
        # 遍历import: 只有workflow中有import， task里面没有也不应该有import
        if not self.workflow_processor.imports:
            return None

        platform = "default" if not self.PLATFORM else self.PLATFORM
        filename = pathlib.Path(path)/f"bundle.zip"
        z: zipfile.ZipFile = existsZip
        if not z:
            if os.path.exists(filename):
                os.remove(filename)
            z = zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED)

        for import_item in self.workflow_processor.imports.values():
            wdl = import_item.wdl

            # 打包导入文件到tar中
            dirname = os.path.dirname(import_item.path) + '/'
            if dirname not in z.namelist():
                # print('add path', dirname)
                zipinfo_dir = zipfile.ZipInfo(dirname)
                zipinfo_dir.compress_type = zipfile.ZIP_STORED
                zipinfo_dir.external_attr = 0o40755 << 16       # permissions drwxr-xr-x
                zipinfo_dir.external_attr |= 0x10               # MS-DOS directory flag
                z.writestr(zipinfo_dir, '')


            zipinfo = zipfile.ZipInfo(import_item.path)
            zipinfo.external_attr = 0o644 << 16                 # permissions -r-wr--r--
            
            # click.secho(f"in base zip_import_file: path[{wdl.fileWdl}] id[{id(wdl)}]", fg='green')
            z.writestr(zipinfo, str(wdl))
            # print(str(wdl))

        if not existsZip:
            z.close()

        return filename

    def submit(self):
        host = self.backend_config['host']

        wdl = os.path.basename(self.workflow_processor.fileWdl)
        input_json = os.path.splitext(os.path.basename(self.input_processor.filepath))[0] + ".json"

        files = {
            "workflowSource": (wdl, self.stream_workflow),
            "workflowInputs": (input_json, self.stream_input),
            "workflowDependencies": ("bundle.zip", self.stream_bundle)
        }

        rsp = requests.post(f"{host}/api/workflows/v1", files=files)
        rsp_data = rsp.json()
        return rsp_data['id']

    def metadata(self, cromwell_id: str):
        host = self.backend_config['host']

        rsp = requests.get(f"{host}/api/workflows/v1/{cromwell_id}/metadata")
        return rsp.json()