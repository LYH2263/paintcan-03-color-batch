"""色号批次模块。

测算时确定本单色号（请求显式给出优先，缺省回退设置中的默认色号），
并把色号连同当时的净面积、升数、涂布率、遍数钉选为不可变快照，
随测算结果写入 calc_runs，使之后修改默认色号不影响历史记录。
"""

DEFAULT_COLOR_KEY = "default_color_code"
FALLBACK_DEFAULT_COLOR = "N001"


def normalize(color_code):
    """去掉首尾空白；None 表示请求未携带该字段。"""
    if color_code is None:
        return None
    return str(color_code).strip()


def resolve_color(color_code, default_color):
    """解析本单实际使用的色号。

    - 请求显式给了非空白色号：原样（去空白后）使用；
    - 请求缺省（None）：使用设置中的默认色号；
    - 显式给出空串或仅空白、或默认色号也为空：拒绝整单（ValueError）。
    """
    code = normalize(color_code)
    if code is None:
        code = normalize(default_color) or ""
    if not code:
        raise ValueError("色号不能为空")
    return code


def pin_snapshot(color_code, result):
    """把色号与测算当下的关键数值钉选为快照。"""
    return {
        "color_code": color_code,
        "net_m2": result["net_m2"],
        "liters": result["liters"],
        "coverage": result["coverage"],
        "coats": result["coats"],
    }
