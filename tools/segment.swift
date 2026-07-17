import Vision
import CoreImage
import AppKit

let inPath = CommandLine.arguments[1]
let outPath = CommandLine.arguments[2]

guard let ciImage = CIImage(contentsOf: URL(fileURLWithPath: inPath)) else {
    fatalError("cannot load \(inPath)")
}

let request = VNGeneratePersonSegmentationRequest()
request.qualityLevel = .accurate
request.outputPixelFormat = kCVPixelFormatType_OneComponent8

let handler = VNImageRequestHandler(ciImage: ciImage, options: [:])
try handler.perform([request])

guard let mask = request.results?.first?.pixelBuffer else {
    fatalError("no segmentation result")
}

var maskImage = CIImage(cvPixelBuffer: mask)
// scale mask up to source size
let sx = ciImage.extent.width / maskImage.extent.width
let sy = ciImage.extent.height / maskImage.extent.height
maskImage = maskImage.transformed(by: CGAffineTransform(scaleX: sx, y: sy))

// composite: person over white background using the mask
let white = CIImage(color: .white).cropped(to: ciImage.extent)
let blend = CIFilter(name: "CIBlendWithMask", parameters: [
    kCIInputImageKey: ciImage,
    kCIInputBackgroundImageKey: white,
    kCIInputMaskImageKey: maskImage,
])!
let output = blend.outputImage!

let ctx = CIContext()
let cg = ctx.createCGImage(output, from: output.extent)!
let rep = NSBitmapImageRep(cgImage: cg)
let png = rep.representation(using: .png, properties: [:])!
try png.write(to: URL(fileURLWithPath: outPath))
print("wrote \(outPath)")