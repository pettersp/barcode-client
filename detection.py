import cv2
from pyzbar.pyzbar import decode


def detect_barcode(frame):
    detected_barcodes = decode(frame)
    if not detected_barcodes:
        print("\n No barcode! \n")
        return frame, False

    else:
        for barcode in detected_barcodes:
            print(barcode.data)
            (x, y, w, h) = barcode.rect
            cv2.rectangle(frame, (x - 10, y - 10),
                          (x + w + 10, y + h + 10),
                          (0, 255, 0), 2)

        if detected_barcodes[0]:
            return frame, detected_barcodes[0].data