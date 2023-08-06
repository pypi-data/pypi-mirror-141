# from abc import abstractmethod
# from typing import Any, Generic, Sequence, Tuple, TypeVar, Union, overload

# from reparsec.core import combinators, types

# A = TypeVar("A")
# B = TypeVar("B")
# C = TypeVar("C")
# D = TypeVar("D")
# Self = TypeVar("Self", bound="_Parser[Any, Any]")


# class _Parser(Generic[A, B]):
#     def __init__(self, parse_fn: types.ParseFn[Sequence[A], B]):
#         self.name = ""
#         self._parse_fn = parse_fn

#     def named(self: Self, name: str) -> Self:
#         self.name = name
#         return self

#     def define(self, p: "_Parser[A, B]") -> None:
#         self._parse_fn = p._parse_fn
#         self.named(p.name)

#     def parse(self, tokens: Sequence[A]) -> B:
#         r = self._parse_fn(tokens, 0, )


# class _IgnoredParser(_Parser[A, None]):
#     @overload
#     def __add__(self, other: "Parser[A, C]") -> "Parser[A, C]": ...
#     @overload
#     def __add__(self, other: "_IgnoredParser[A]") -> "_IgnoredParser[A]": ...

#     @overload
#     def __add__(
#             self, other: "_TupleParser[A, C, D]") -> "_TupleParser[A, C, D]":
#         ...

#     @abstractmethod
#     def __add__(
#             self,
#             other: Union[
#                 "Parser[A, C]", "_IgnoredParser[A]", "_TupleParser[A, C, D]"
#             ]
#     ) -> Union["Parser[A, C]", "_IgnoredParser[A]", "_TupleParser[A, C, D]"]:
#         ...


# class _TupleParser(_Parser[A, Tuple[B, C]]):
#     @overload
#     def __add__(self, other: "Parser[A, Any]") -> "Parser[A, Any]": ...

#     @overload
#     def __add__(self, other: _IgnoredParser[A]) -> "_TupleParser[A, B, C]":
#        ...

#     @overload
#     def __add__(
#             self,
#             other: "_TupleParser[A, Any, Any]") -> "Parser[A, Any]":
#         ...

#     @abstractmethod
#     def __add__(
#         self,
#         other: Union[
#             "Parser[A, Any]",
#             _IgnoredParser[A],
#             "_TupleParser[A, Any, Any]"
#         ]
#     ) -> Union["Parser[A, Any]", "_TupleParser[A, B, C]"]: ...


# class Parser(_Parser[A, B]):
#     @overload
#     def __add__(self, other: "Parser[A, C]") -> _TupleParser[A, B, C]: ...
#     @overload
#     def __add__(self, other: _IgnoredParser[A]) -> "Parser[A, B]": ...

#     @overload
#     def __add__(self, other: _TupleParser[A, Any, Any]) -> "Parser[A, Any]":
#         ...

#     @abstractmethod
#     def __add__(
#         self,
#         other: Union[
#             "Parser[A, C]", _IgnoredParser[A], _TupleParser[A, Any, Any]
#         ]
#     ) -> Union[_TupleParser[A, B, C], "Parser[A, B]", "Parser[A, Any]"]: ...
