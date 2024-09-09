class env:
  #DRIVERS FOR SELENIUM
  CHROMEDRIVER_PACKAGE_LINUX = "https://storage.googleapis.com/chrome-for-testing-public/128.0.6613.86/linux64/chrome-linux64.zip"
  CHROMEDRIVER_PACKAGE_W64 = "https://storage.googleapis.com/chrome-for-testing-public/128.0.6613.86/win64/chrome-win64.zip"
  CHROMEDRIVER_PACKAGE_MACOS64="https://storage.googleapis.com/chrome-for-testing-public/128.0.6613.86/mac-x64/chrome-mac-x64.zip"
  DRIVER_PATH="./controller/chromedriver"
  DRIVER_NAME="chromedriver"
  
  #MINECRAFT SERVER
  SERVER_DIR="./Server"
  ATTR="-Xmx12G -Xms2048M -jar "
  EXE_COMMAND=f"java {ATTR} server.jar  nogui"