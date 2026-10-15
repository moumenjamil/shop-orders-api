# shop-orders-api

The shop's orders service. It writes the `orders` table of the shop
database (Neon `shop`, `public.orders`), which the data team's
`orders_daily` pipeline (moumenjamil/orders-data) reads every night.

- `app/orders.py`: order statuses and every write to `orders`
- `app/api.py`: the HTTP endpoints
- `migrations/`: the table, as the app owns it
