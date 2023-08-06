from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=['app/core/config/settings.toml', 'app/core/config/.secrets.toml'],
    environments=True,
    ENV_FOR_DYNACONF="develop"  # 修改默认使用的环境，默认为：[development]
)
