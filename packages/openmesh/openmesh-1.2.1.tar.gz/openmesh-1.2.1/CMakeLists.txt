cmake_minimum_required(VERSION 3.3.0)

project(openmesh          
        VERSION 1.2.1
        LANGUAGES CXX )

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

add_subdirectory(OpenMesh)
add_subdirectory(pybind11)

if (NOT WIN32)
	set_target_properties(
		OpenMeshCore OpenMeshTools PROPERTIES
		EXCLUDE_FROM_ALL ON
		EXCLUDE_FROM_DEFAULT_BUILD ON
	)
endif ()

set( HEADERS
src/Circulator.hh
src/Decimater.hh
src/InputOutput.hh
src/Iterator.hh
src/Mesh.hh
src/MeshTypes.hh
src/Miscellaneous.hh
src/Utilities.hh
)

set( SOURCES
src/Bindings.cc
src/InputOutput.cc
src/Miscellaneous.cc
)

pybind11_add_module(openmesh ${HEADERS} ${SOURCES})

if (WIN32)
	target_link_libraries(openmesh PRIVATE OpenMeshCore)
	target_link_libraries(openmesh PRIVATE OpenMeshTools)
	target_compile_definitions(openmesh PRIVATE _USE_MATH_DEFINES)
else ()
	target_link_libraries(openmesh PRIVATE OpenMeshCoreStatic)
	target_link_libraries(openmesh PRIVATE OpenMeshToolsStatic)
endif ()

enable_testing()
add_test(
	NAME discover_tests
	COMMAND ${PYTHON_EXECUTABLE} -m unittest discover --failfast
	WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/tests
)
set_tests_properties(
	discover_tests PROPERTIES
	ENVIRONMENT "PYTHONPATH=$<TARGET_FILE_DIR:openmesh>"
)
