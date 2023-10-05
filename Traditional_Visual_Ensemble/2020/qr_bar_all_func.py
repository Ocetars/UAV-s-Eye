import cv2
import numpy as np

def detect_qrcode(frame):
    # 设置检测器
    qrcoder = cv2.QRCodeDetector()
    # 检测识别二维码
    codeinfo, points, straight_qrcode = qrcoder.detectAndDecode(frame)

    # 如果识别到二维码
    if codeinfo:
        result = np.copy(frame)
        cv2.drawContours(result, [np.int32(points)], 0, (0, 0, 255), 2)
        # 返回识别到二维码的图片和信息
        return result, codeinfo
    else:
        # 返回原始的摄像头画面和 None
        return frame, None

def detect_barcode(frame):
    # 创建条形码检测器
    detect_obj = cv2.barcode_BarcodeDetector()  # type: ignore

    # 检测条形码
    is_ok, bar_info, bar_type, points = detect_obj.detectAndDecode(frame)

    # 如果检测到条形码，返回条形码信息和图像
    if is_ok:
        result = np.copy(frame)
        x1 = int(points[0][1][0])  # 左上x
        y1 = int(points[0][1][1])  # 左上y
        x2 = int(points[0][3][0])  # 右下x
        y2 = int(points[0][3][1])  # 右下y
        cv2.rectangle(result, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(
            result,
            str(bar_info),
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 0, 255),
            2,
        )
        # 返回识别到条形码的图片和信息
        return result, bar_info
    else:
        # 返回原始的摄像头画面和 None
        return frame, None

def detect_allcode(frame):
    # 设置二维码检测器
    qrcoder = cv2.QRCodeDetector()
    # 创建条形码检测器
    detect_obj = cv2.barcode_BarcodeDetector() # type: ignore

    # 检测识别二维码
    codeinfo, QRpoints, straight_qrcode = qrcoder.detectAndDecode(frame)
    # 检测识别条形码
    result = detect_obj.detectAndDecode(frame)
    is_ok, bar_info, bar_type, BARpoints = result

    # 如果识别到二维码
    if codeinfo:
        result = np.copy(frame)
        cv2.drawContours(result, [np.int32(QRpoints)], 0, (0, 0, 255), 2)
        # 返回识别到二维码的图片和信息
        return result, codeinfo
    # 如果识别到条形码
    elif is_ok:
        result = np.copy(frame)
        x1 = int(BARpoints[0][1][0])  # 左上x
        y1 = int(BARpoints[0][1][1])  # 左上y
        x2 = int(BARpoints[0][3][0])  # 右下x
        y2 = int(BARpoints[0][3][1])  # 右下y
        cv2.rectangle(result, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(
            result,
            str(bar_info),
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 0, 255),
            2,
        )
        # 返回识别到条形码的图片和信息
        return result, bar_info
    else:
        # 返回原始的摄像头画面和 None
        return frame, None
    
'''
函数将返回两个值，第一个是识别到二维码或条形码后的图像，
第二个是识别到的二维码或条形码信息。
如果没有识别到二维码或条形码，则返回原始的摄像头画面和 None。
'''

if __name__ == "__main__":
    # 打开摄像头
    cap = cv2.VideoCapture(2)
    # 设置摄像头分辨率
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    while True:
        # 读取摄像头画面
        ret, frame = cap.read()
        # 识别二维码
        # result, codeinfo = detect_qrcode(frame)
        # 识别条形码
        result, codeinfo = detect_barcode(frame)
        # 识别二维码和条形码
        # result, codeinfo = detect_allcode(frame)

        # 如果识别到二维码或条形码
        if codeinfo:
            print(codeinfo)

        # 显示画面
        cv2.imshow("capture", result)
        # 按 q 键退出
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # 释放摄像头
    cap.release()
    cv2.destroyAllWindows()