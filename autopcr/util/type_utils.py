from typing import get_origin, get_args, Type
from typing import (
    Type, Any, Optional, get_origin, get_args, TypeVar, _GenericAlias
)
import inspect

def _substitute_typevars(tp: Any, mapping: dict) -> Any:
    if isinstance(tp, TypeVar):
        return mapping.get(tp, tp)
    origin = get_origin(tp)
    if origin is not None:
        args = get_args(tp)
        new_args = tuple(_substitute_typevars(a, mapping) for a in args)
        try:
            return origin[new_args]
        except Exception:
            return _GenericAlias(origin, new_args)
    return tp

def find_type_base(
    cls: Type,
    target_generic: Type
) -> Optional[Any]:
    """
    在 cls 的继承链中寻找第一个形如 target_generic[T] 的基类，
    返回完整替换后的 T（可能是嵌套泛型）。
    """
    # 队列中元素: (当前“类或泛型基类表达式”，当前 TypeVar->实参 映射)
    queue = [(cls, {})]
    visited = set()

    while queue:
        base_expr, var_map = queue.pop(0)
        if base_expr in visited:
            continue
        visited.add(base_expr)

        # 对于一个类或泛型别名，都用 __orig_bases__（若无则 __bases__）拿到下一层
        origin_cls = get_origin(base_expr) or base_expr
        orig_bases = getattr(origin_cls, "__orig_bases__", origin_cls.__bases__)

        for raw_base in orig_bases:
            # raw_base 是一个可能带泛型实参的类型表达式
            origin = get_origin(raw_base) or raw_base
            args   = get_args(raw_base)

            # 构建这条边上新的 TypeVar 映射
            new_map = var_map.copy()
            parameters = getattr(origin, "__parameters__", ())
            for param, arg in zip(parameters, args):
                # 先把 arg 里的旧 TypeVar 替换一下
                new_map[param] = _substitute_typevars(arg, var_map)

            # 如果这个基类就是我们要找的那种 RequestBase[…]
            if origin is target_generic:
                # raw_base 的 args[0] 已经被 new_map 替换完毕
                will_return = _substitute_typevars(args[0], var_map)

                if hasattr(will_return, '__parameters__'):
                    # 如果是泛型，返回这个泛型的实例
                    param = tuple(
                        _substitute_typevars(arg, var_map) for arg in will_return.__parameters__
                    )
                    return will_return[param]
                else:
                    # 否则直接返回
                    return will_return

            # 否则把 “带泛型的 raw_base” 自身，和 new_map 入队
            if inspect.isclass(origin) or get_origin(raw_base) is not None:
                queue.append((raw_base, new_map))

    return None
