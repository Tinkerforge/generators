@rem windows command shell batch script
if not exist "build" mkdir build
cmake -E chdir build/ cmake -G "MinGW Makefiles" -DCMAKE_MAKE_PROGRAM:PATH=make.exe -DCMAKE_TOOLCHAIN_FILE=../src/bricklib2/cmake/toolchains/arm-none-eabi.cmake ../
