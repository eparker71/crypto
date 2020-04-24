update data
set [Quantity Transacted] = [Quantity Transacted] * -1
where [Transaction Type] = 'Sell';

update data
set [USD Total (inclusive of fees)] = [USD Total (inclusive of fees)] * -1
where [Transaction Type] = 'Sell';


