SELECT
    c.customer_id,
    c.name AS customer_name,
    o.order_id,
    o.order_date,
    o.total_amount,
    p.method AS payment_method,
    p.amount AS payment_amount,
    s.status AS shipment_status,
    s.shipment_date
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
INNER JOIN payments p ON o.order_id = p.order_id
INNER JOIN shipments s ON o.order_id = s.order_id
ORDER BY o.order_date DESC;
