  """
  MCP adapter for the pizza agent.

  This module dynamically loads `pizza.py` (next to this file) and exposes
  simple wrappers for the endpoint-like functions so other code can call them
  in a consistent way.

  Exported names:
  - get_pizzas, get_pizza_by_id, get_toppings, get_topping_by_id,
    get_topping_categories, get_orders, get_order_by_id, place_order,
    delete_order_by_id

  Usage example:
      from myagent import mcp
      mcp.get_pizzas()

  This dynamic-loader approach avoids requiring `myagent` to be a proper
  package with `__init__.py` in environments where imports might fail.
  """

  import os
  import importlib.util
  from typing import Any, Dict, List, Optional

  # Load pizza.py located in the same directory as this file
  THIS_DIR = os.path.dirname(__file__)
  PIZZA_PATH = os.path.join(THIS_DIR, "pizza.py")
  _spec = importlib.util.spec_from_file_location("pizza_module", PIZZA_PATH)
  _pizza_mod = importlib.util.module_from_spec(_spec)
  _spec.loader.exec_module(_pizza_mod)  # type: ignore

  # Wrapper functions

  def get_pizzas() -> List[Dict[str, Any]]:
      """Return list of pizzas."""
      return _pizza_mod.get_pizzas()


  def get_pizza_by_id(pizza_id: int) -> Optional[Dict[str, Any]]:
      """Return a pizza by id."""
      return _pizza_mod.get_pizza_by_id(pizza_id)


  def get_toppings() -> List[Dict[str, Any]]:
      """Return list of toppings."""
      return _pizza_mod.get_toppings()


  def get_topping_by_id(topping_id: int) -> Optional[Dict[str, Any]]:
      """Return a topping by id."""
      return _pizza_mod.get_topping_by_id(topping_id)


  def get_topping_categories() -> List[str]:
      """Return topping categories."""
      return _pizza_mod.get_topping_categories()


  def get_orders() -> List[Dict[str, Any]]:
      """Return all orders."""
      return _pizza_mod.get_orders()


  def get_order_by_id(order_id: int) -> Optional[Dict[str, Any]]:
      """Return an order by id."""
      return _pizza_mod.get_order_by_id(order_id)


  def place_order(order_data: Dict[str, Any]) -> Dict[str, Any]:
      """Place a new order. Expects the same shape as `pizza.place_order`.

      Example: {"userId": "u1", "items": [{"pizzaId": 2, "qty": 1}]}
      """
      return _pizza_mod.place_order(order_data)


  def delete_order_by_id(order_id: int, user_id: Any) -> Dict[str, Any]:
      """Cancel an order if allowed. Delegates to `pizza.delete_order_by_id`."""
      return _pizza_mod.delete_order_by_id(order_id, user_id)


  # A simple registry mapping endpoint names to callables for convenience
  METHODS = {
      "get_pizzas": get_pizzas,
      "get_pizza_by_id": get_pizza_by_id,
      "get_toppings": get_toppings,
      "get_topping_by_id": get_topping_by_id,
      "get_topping_categories": get_topping_categories,
      "get_orders": get_orders,
      "get_order_by_id": get_order_by_id,
      "place_order": place_order,
      "delete_order_by_id": delete_order_by_id,
  }


  if __name__ == "__main__":
      # quick smoke demonstration when run directly
      print("Pizzas:", get_pizzas())
      print("Toppings:", get_toppings())
      # create a sample order and then cancel it
      ordn = place_order({"userId": "demo", "items": [{"pizzaId": 1, "qty": 1}]})
      print("Created order:", ordn)
      cancelled = delete_order_by_id(ordn["id"], "demo")
      print("Cancelled order:", cancelled)
