import rds2py

# parsed_obj = rds2py.PyParsedObject("tests/data/s4_dense_matrix.rds")
robj = rds2py.read_rds("tests/test.rds")
# print(parsed_obj)

# robject_obj = parsed_obj.get_robject()
# # print(robject_obj)

# # print(robject_obj.get_rtype())

# actual_arrau = robject_obj.realize_value()
# # print(actual_arrau)

# # mat = rds2py.as_dense_matrix(actual_arrau)
# # print(mat)

# # print("############")
# # print(actual_arrau["class_name"])
# # print(robject_obj)

# # print(actual_arrau["class_name"])
# # print(robject_obj)

sce = rds2py.as_SCE(robj)
print(sce)

# actual_arrau_names = robject_obj.get_attribute_names()
# print(actual_arrau_names)


# attr_values = robject_obj.realize_attr_value()
# print(attr_values)

# dims = robject_obj.get_dimensions()
# print(dims)