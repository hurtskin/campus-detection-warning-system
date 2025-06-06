@REM ----------------------------------------------------------------------------
@REM  Copyright 2001-2006 The Apache Software Foundation.
@REM
@REM  Licensed under the Apache License, Version 2.0 (the "License");
@REM  you may not use this file except in compliance with the License.
@REM  You may obtain a copy of the License at
@REM
@REM       http://www.apache.org/licenses/LICENSE-2.0
@REM
@REM  Unless required by applicable law or agreed to in writing, software
@REM  distributed under the License is distributed on an "AS IS" BASIS,
@REM  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
@REM  See the License for the specific language governing permissions and
@REM  limitations under the License.
@REM ----------------------------------------------------------------------------
@REM
@REM   Copyright (c) 2001-2006 The Apache Software Foundation.  All rights
@REM   reserved.

@echo off

set ERROR_CODE=0

:init
@REM Decide how to startup depending on the version of windows

@REM -- Win98ME
if NOT "%OS%"=="Windows_NT" goto Win9xArg

@REM set local scope for the variables with windows NT shell
if "%OS%"=="Windows_NT" @setlocal

@REM -- 4NT shell
if "%eval[2+2]" == "4" goto 4NTArgs

@REM -- Regular WinNT shell
set CMD_LINE_ARGS=%*
goto WinNTGetScriptDir

@REM The 4NT Shell from jp software
:4NTArgs
set CMD_LINE_ARGS=%$
goto WinNTGetScriptDir

:Win9xArg
@REM Slurp the command line arguments.  This loop allows for an unlimited number
@REM of arguments (up to the command line limit, anyway).
set CMD_LINE_ARGS=
:Win9xApp
if %1a==a goto Win9xGetScriptDir
set CMD_LINE_ARGS=%CMD_LINE_ARGS% %1
shift
goto Win9xApp

:Win9xGetScriptDir
set SAVEDIR=%CD%
%0\
cd %0\..\.. 
set BASEDIR=%CD%
cd %SAVEDIR%
set SAVE_DIR=
goto repoSetup

:WinNTGetScriptDir
for %%i in ("%~dp0..") do set "BASEDIR=%%~fi"

:repoSetup
set REPO=


if "%JAVACMD%"=="" set JAVACMD=java

if "%REPO%"=="" set REPO=%BASEDIR%\lib

set CLASSPATH="%BASEDIR%"\etc;"%REPO%"\neo4j-java-driver-5.26.0.jar;"%REPO%"\reactive-streams-1.0.4.jar;"%REPO%"\netty-handler-4.1.115.Final.jar;"%REPO%"\netty-common-4.1.115.Final.jar;"%REPO%"\netty-resolver-4.1.115.Final.jar;"%REPO%"\netty-buffer-4.1.115.Final.jar;"%REPO%"\netty-transport-4.1.115.Final.jar;"%REPO%"\netty-transport-native-unix-common-4.1.115.Final.jar;"%REPO%"\netty-codec-4.1.115.Final.jar;"%REPO%"\netty-tcnative-classes-2.0.69.Final.jar;"%REPO%"\reactor-core-3.6.10.jar;"%REPO%"\cypher-antlr-ast-common-5.26.0.jar;"%REPO%"\antlr4-runtime-4.13.2.jar;"%REPO%"\cypher-antlr-common-5.26.0.jar;"%REPO%"\cypher-parser-ast-common-5.26.0.jar;"%REPO%"\neo4j-util-5.26.0.jar;"%REPO%"\neo4j-exceptions-5.26.0.jar;"%REPO%"\neo4j-common-5.26.0.jar;"%REPO%"\commons-text-1.12.0.jar;"%REPO%"\eclipse-collections-11.1.0.jar;"%REPO%"\eclipse-collections-api-11.1.0.jar;"%REPO%"\commons-lang3-3.17.0.jar;"%REPO%"\scala-library-2.13.11.jar;"%REPO%"\cypher-v5-ast-factory-5.26.0.jar;"%REPO%"\neo4j-ast-5.26.0.jar;"%REPO%"\neo4j-expressions-5.26.0.jar;"%REPO%"\caffeine-3.1.8.jar;"%REPO%"\cypher-v5-antlr-parser-5.26.0.jar;"%REPO%"\cypher-v5-parser-listener-5.26.0.jar;"%REPO%"\cypher-parser-common-5.26.0.jar;"%REPO%"\neo4j-gql-status-5.26.0.jar;"%REPO%"\annotations-5.26.0.jar;"%REPO%"\jackson-databind-2.18.0.jar;"%REPO%"\jackson-annotations-2.18.0.jar;"%REPO%"\jackson-core-2.18.0.jar;"%REPO%"\neo4j-cypher-macros-5.26.0.jar;"%REPO%"\scala-reflect-2.13.11.jar;"%REPO%"\cypher-v5-literal-interpreter-5.26.0.jar;"%REPO%"\neo4j-values-5.26.0.jar;"%REPO%"\neo4j-graphdb-api-5.26.0.jar;"%REPO%"\neo4j-resource-5.26.0.jar;"%REPO%"\neo4j-collections-5.26.0.jar;"%REPO%"\neo4j-unsafe-5.26.0.jar;"%REPO%"\jna-5.15.0.jar;"%REPO%"\neo4j-cypher-dsl-2024.2.0.jar;"%REPO%"\argparse4j-0.9.0.jar;"%REPO%"\jline-terminal-3.21.0.jar;"%REPO%"\jline-reader-3.21.0.jar;"%REPO%"\jline-terminal-jansi-3.21.0.jar;"%REPO%"\jansi-2.4.0.jar;"%REPO%"\cypher-shell-5.26.0.jar

set ENDORSED_DIR=
if NOT "%ENDORSED_DIR%" == "" set CLASSPATH="%BASEDIR%"\%ENDORSED_DIR%\*;%CLASSPATH%

if NOT "%CLASSPATH_PREFIX%" == "" set CLASSPATH=%CLASSPATH_PREFIX%;%CLASSPATH%

@REM Reaching here means variables are defined and arguments have been captured
:endInit

%JAVACMD% %JAVA_OPTS%  -classpath %CLASSPATH% -Dapp.name="cypher-shell" -Dapp.repo="%REPO%" -Dapp.home="%BASEDIR%" -Dbasedir="%BASEDIR%" org.neo4j.shell.startup.CypherShellBoot %CMD_LINE_ARGS%
if %ERRORLEVEL% NEQ 0 goto error
goto end

:error
if "%OS%"=="Windows_NT" @endlocal
set ERROR_CODE=%ERRORLEVEL%

:end
@REM set local scope for the variables with windows NT shell
if "%OS%"=="Windows_NT" goto endNT

@REM For old DOS remove the set variables from ENV - we assume they were not set
@REM before we started - at least we don't leave any baggage around
set CMD_LINE_ARGS=
goto postExec

:endNT
@REM If error code is set to 1 then the endlocal was done already in :error.
if %ERROR_CODE% EQU 0 @endlocal


:postExec

if "%FORCE_EXIT_ON_ERROR%" == "on" (
  if %ERROR_CODE% NEQ 0 exit %ERROR_CODE%
)

exit /B %ERROR_CODE%
