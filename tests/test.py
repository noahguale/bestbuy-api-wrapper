
from client import BestBuy

bb = BestBuy()

test = bb.ProductAPI.search_sku(sku=5721600).regularPrice    
# test2 = bb.ProductAPI.search(searchTerm="laptop", onSale="true")
# test3 = bb.StoreAPI.search_by_city(city="Atlanta")[0].json
# bb.CategoryAPI.search_by_category_id(category_id="abcat0011001")

print(test)