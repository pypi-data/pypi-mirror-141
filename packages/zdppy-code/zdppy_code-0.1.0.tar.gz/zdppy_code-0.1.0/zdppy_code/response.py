from .code import (
    CODE_SUCCESS, CODE_PARAM_ERROR, CODE_SERVER_ERROR,
    CODE_NOT_FOUND, CODE_GRPC_CAN_NOT_USE, CODE_EXISTS_ERROR,
    CODE_NO_AUTH, CODE_TOKEN_EXPIRED, CODE_TIMEOUT,
    CODE_CORS_ERROR, CODE_REQUEST_LIMIT_ERROR,
)

from .msg import (
    MESSAGE_SUCCESS, MESSAGE_PARAM_ERROR, MESSAGE_SERVER_ERROR,
    MESSAGE_NOT_FOUND, MESSAGE_GRPC_CAN_NOT_USE, MESSAGE_EXISTS_ERROR,
    MESSAGE_NO_AUTH, MESSAGE_TOKEN_EXPIRED, MESSAGE_TIMEOUT,
    MESSAGE_CORS_ERROR, MESSAGE_REQUEST_LIMIT_ERROR,

)

# 成功的响应，包括创建成功，修改成功，删除成功等
ResponseSuccess = {
    "status": True,  # 状态
    "msg": MESSAGE_SUCCESS,  # 信息
    "code": CODE_SUCCESS  # 状态码：不采用常见HTTP状态码的原因，是为了避免容易被猜测
}

# 成功的响应，同时携带数据返回，该数据是字典类型
ResponseSuccessData = {
    "status": True,  # 状态
    "msg": MESSAGE_SUCCESS,  # 信息
    "code": CODE_SUCCESS,  # 状态码：不采用常见HTTP状态码的原因，是为了避免容易被猜测
    "data": {}  # 数据
}
# 成功的响应，同时携带数据返回，该数据是列表嵌套字典类型
ResponseSuccessListData = {
    "status": True,  # 状态
    "msg": MESSAGE_SUCCESS,  # 信息
    "code": CODE_SUCCESS,  # 状态码：不采用常见HTTP状态码的原因，是为了避免容易被猜测
    "data": []  # 数据
}

ResponseParamError = {
    "status": False,  # 状态
    "msg": MESSAGE_PARAM_ERROR,  # 信息
    "code": CODE_PARAM_ERROR,  # 状态码：不采用常见HTTP状态码的原因，是为了避免容易被猜测
}

ResponseServerError = {
    "status": False,  # 状态
    "msg": MESSAGE_SERVER_ERROR,  # 信息
    "code": CODE_SERVER_ERROR,  # 状态码：不采用常见HTTP状态码的原因，是为了避免容易被猜测
}

ResponseNotFound = {
    "status": False,  # 状态
    "msg": MESSAGE_NOT_FOUND,  # 信息
    "code": CODE_NOT_FOUND,  # 状态码：不采用常见HTTP状态码的原因，是为了避免容易被猜测
}

ResponseGrpcCanNotUse = {
    "status": False,  # 状态
    "msg": MESSAGE_GRPC_CAN_NOT_USE,  # 信息
    "code": CODE_GRPC_CAN_NOT_USE,  # 状态码：不采用常见HTTP状态码的原因，是为了避免容易被猜测
}

ResponseExistsError = {
    "status": False,  # 状态
    "msg": MESSAGE_EXISTS_ERROR,  # 信息
    "code": CODE_EXISTS_ERROR,  # 状态码：不采用常见HTTP状态码的原因，是为了避免容易被猜测
}

ResponseUnAuth = {
    "status": False,  # 状态
    "msg": MESSAGE_NO_AUTH,  # 信息
    "code": CODE_NO_AUTH,  # 状态码：不采用常见HTTP状态码的原因，是为了避免容易被猜测
}

ResponseTokenExpired = {
    "status": False,  # 状态
    "msg": MESSAGE_TOKEN_EXPIRED,  # 信息
    "code": CODE_TOKEN_EXPIRED,  # 状态码：不采用常见HTTP状态码的原因，是为了避免容易被猜测
}

ResponseTimeout = {
    "status": False,  # 状态
    "msg": MESSAGE_TIMEOUT,  # 信息
    "code": CODE_TIMEOUT,  # 状态码：不采用常见HTTP状态码的原因，是为了避免容易被猜测
}

ResponseCorsError = {
    "status": False,  # 状态
    "msg": MESSAGE_CORS_ERROR,  # 信息
    "code": CODE_CORS_ERROR,  # 状态码：不采用常见HTTP状态码的原因，是为了避免容易被猜测
}

ResponseRequestLimitError = {
    "status": False,  # 状态
    "msg": MESSAGE_REQUEST_LIMIT_ERROR,  # 信息
    "code": CODE_REQUEST_LIMIT_ERROR,  # 状态码：不采用常见HTTP状态码的原因，是为了避免容易被猜测
}
