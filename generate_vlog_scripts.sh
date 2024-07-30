#!/bin/bash

# 定义固定路径和变量/ Define fixed paths and variables
VLOG_QUERY_PATH="~/project/vlog/vlog_query.py"
BIN_DIR="/usr/local/bin"

# 定义脚本名称和配置文件路径的映射/ Define script names and their corresponding configuration file paths
declare -A SCRIPTS_MAP=(
    ["qbvlog"]="~/project/vlog/business.toml"
    ["qtvlog"]="~/project/vlog/traefik.toml"
    # 你可以在这里继续添加更多的映射，例如/ You can add more mappings here, for example:
    # ["qcvlog"]="~/project/vlog/another_config.toml"
)

# 先删除已有的文件/ Remove existing files first
for script in "${!SCRIPTS_MAP[@]}"; do
    rm -f "$BIN_DIR/$script"
done

# 创建新的脚本文件并移动到指定目录/ Create new script files and move them to the specified directory
for script in "${!SCRIPTS_MAP[@]}"; do
    echo '#!/bin/bash' > "$script"
    echo "python3 $VLOG_QUERY_PATH --conf ${SCRIPTS_MAP[$script]} \"\$@\"" >> "$script"
    chmod +x "$script"
    mv "$script" "$BIN_DIR/"
done

