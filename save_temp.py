import similarity

# Save temporary plate after handle plate text
def save_temp(plateNumberDict, text_plate):
    similar_plate_count = 0
    if len(plateNumberDict) > 0:

        # Kiểm tra biển số hiện tại có tương đồng với các biển số trong Dict hay không ?
        for plate in plateNumberDict.keys():
            if similarity.plate_similarity(str(text_plate), str(plate)) > 0.7:
                similar_plate_count += 1

        # Kiểm tra biển số đã được kiểm tra
        process = open("process.txt", "r")

        # Nếu không tương đồng 1 trong số biển số hoắc đã kiểm tra thành công sẽ clear Dict
        if similar_plate_count != len(plateNumberDict) or process.read() == 'DONE':
            plateNumberDict.clear()
            print('CLEAR DICT')
            if similar_plate_count != len(plateNumberDict):
                processw = open("process.txt", "w")
                processw.write("DETECTING")
                processw.close()

    preplate = open("preplate.txt", "r")
    if (not similarity.plate_similarity(str(text_plate), str(preplate.read())) > 0.7):
        # Lưu biển số vào Dict
        if text_plate in plateNumberDict.keys():
            plateNumberDict[str(text_plate)] += 1
        else:
            plateNumberDict[str(text_plate)] = 1

        plateNumberDict = dict(sorted(plateNumberDict.items(), key=lambda item: item[1], reverse=True))

        # Lưu danh sách list biển số tạm của 1 biển số vào file temp
        temp = open("temp.txt", "w")
        temp.write(str(next(iter(plateNumberDict.keys()))) + '-' + str(next(iter(plateNumberDict.values()))))
        temp.close()