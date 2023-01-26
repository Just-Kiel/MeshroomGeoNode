import argparse
import convertWgs84ToLambert93
import downloadLidarFromCSV
import unzip_archive
import LAZtoLAS
import getRegion
import download_scan3d_from_csv
import logging

ap = argparse.ArgumentParser()
ap.add_argument("--GPSFile", help="GPSFile", type=str)
ap.add_argument("--resolution", help="resolution", type=str)
ap.add_argument("--outputFolder", help="outputFolder", type=str)
args = ap.parse_args()

logging.basicConfig(level=logging.INFO)

def main():
    logging.info("3D Map !")

    if float(args.resolution) == 0.3:
        logging.info(f"Get Lidar Data")

        lambertCoord = convertWgs84ToLambert93.convertGPSDataToLambert93(args.GPSFile)
        logging.info(f"Lambert Coordinates : {lambertCoord}")

        fpZipArchive = downloadLidarFromCSV.download(lambertCoord, args.outputFolder)
        logging.info(f"Zip Archive : {fpZipArchive}")

        fpUnzipArchive = unzip_archive.unzip(fpZipArchive, args.outputFolder)
        logging.info(f"Unzip Archive : {fpUnzipArchive}")

        LAZtoLAS.convert(fpUnzipArchive, args.outputFolder)

    else :
        logging.info(f"Get RGE or BD Alti Data")

        departementInfo = getRegion.getDepartement(args.GPSFile)
        logging.info(f"Departement : {departementInfo}")

        fpZipArchive = download_scan3d_from_csv.download(departementInfo, float(args.resolution), args.outputFolder)
        logging.info(f"Zip Archive : {fpZipArchive}")

        fpUnzipArchive = unzip_archive.unzip(fpZipArchive, args.outputFolder)
        logging.info(f"Unzip Archive : {fpUnzipArchive}")

        download_scan3d_from_csv.extractFromFolder(fpUnzipArchive, args.outputFolder)
    
    logging.info("3D Map infos downloaded")


if __name__ == "__main__":
    main()