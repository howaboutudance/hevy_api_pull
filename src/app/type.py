"""Type definitions for the application."""

type JSONPrimitive = None | bool | int | float | str
type JSONArray[T] = list[JSONPrimitive | T | "JSONObject"]  # type: ignore
type JSONObject[T] = dict[str, JSONPrimitive | JSONArray | T]  # type: ignore
type JSONType[T] = T | JSONPrimitive | JSONArray | JSONObject
