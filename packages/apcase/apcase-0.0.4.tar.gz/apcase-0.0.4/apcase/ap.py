def allpairs(parameters):
    lines_count = len(parameters)
    line_count = [len(i) for i in parameters]

    keys = [("_%d" % i) for i in range(lines_count)]
    keys_str = ", ".join(keys)

    values = [(" for %s in range(%s)" % (i[0], i[1])) for i in list(zip(keys, line_count))]
    values_str = "".join(values)

    indexs = eval("[(%s)%s]" % (keys_str, values_str))

    elements = ["parameters[%s][i[%s]]" % (i, i) for i in range(lines_count)]
    elements_str = ", ".join(elements)

    return eval("[(%s) for i in indexs]" % elements_str, {"parameters": parameters, "indexs": indexs})



if __name__ == '__main__':
    print(allpairs(parameters=[
        [1, 2, 3],
        [4, 5, 6]
    ]))
