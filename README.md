# nopop

A simple tool that forwards commands to cmd directly, without breaking shell feature, and avoids annoying popup window.


# Description

Here are a few alternative descriptions that are more formal from ChatGPT:

- A command redirection utility: A small tool that forwards commands to the Windows Command Prompt (cmd) without displaying a console window.
- A cmd proxy application: A lightweight software that executes commands in the background without showing a window, providing a seamless interface to the Windows Command Prompt.
- A console-less cmd runner: A compact tool that runs commands in the Windows Command Prompt without popping up a console window, ideal for automated tasks and scripts.
- A background cmd executor: A small utility that executes commands in the Windows Command Prompt without displaying a window, designed for use in automated environments.
- A cmd wrapper application: A lightweight software that wraps commands for the Windows Command Prompt and runs them in the background without showing a window, providing a convenient interface for automated tasks.

# Usage

This tool is primarily designed to work with other programs as a middleware and be called by other programs, for the situations where programs need to call cmd command silently, without trigger cmd's black popup window. For example:

- working with Listary, Everything or FileMenu Tools for custom context menu command
    A frequent requirement is to copy file/folder path backslash auto-escaped to clipboard. This can be done by calling nopop.exe with the following command:

```bash
# for Listary Actions
nohup.exe echo "(action_path)"| sed -e s\#/#g | clip

# for Everything Context Menu
Not available yet. See also: [A UI to customize these commands is still on my TODO list](https://www.voidtools.com/forum/viewtopic.php?t=11399)

# for FileMenu Tools command
nohop.exe echo %FILEPATH1%  | sed -e s#\\#/#g | clip # by busybox echo and sed
nohop.exe powershell -NoProfile -Command "$path='%FILEPATH1%'; $path -replace '\\', '/' | Set-Clipboard" # or by powershell replace

```

-  working with scoop shim add (As a alternative to bat2exe program, which also block popup, by convert bat to exe file instead)

```batch
scoop shim add wcmd nopop "wt.exe -p CMD"
```


# How to build

install builder, then output nopop.exe

``` bash
pip install pyinstaller

pyinstaller --onefile --noconsole nopop.py

```

# How this keeps shell feature?

The shell feature is kept by using the subprocess module with `shell=True` option to run the command in the background without displaying a console window. This allows the user to interact with the command prompt as if they were running the command directly, while the tool handles the execution in the background.

# Why this avoids pop window?

pyinstaller with --noconsole is used for GUI applications to prevent a console window from appearing when the executable is run.


```python
if is_win or is_darwin:
	if not self.console:
		exe = exe + 'w'
```
Source:[PyInstaller](https://github.com/pyinstaller/pyinstaller/blob/919022fa471238de7fb832c81f6c1334b79604ab/PyInstaller/building/api.py#L732-L734)

> Python scripts (files with the extension .py) will be executed by python.exe by default. This executable opens a terminal, which stays open even if the program uses a GUI. If you do not want this to happen, use the extension .pyw which will cause the script to be executed by pythonw.exe by default (both executables are located in the top-level of your Python installation directory). **This suppresses the terminal window on startup**.
>
> You can also make all .py scripts execute with pythonw.exe, setting this through the usual facilities, for example (might require administrative rights):

Source: [3. Using Python on Windows → 3.3.4. Executing scripts](https://docs.python.org/2/using/windows.html#executing-scripts)

```plain
> pyinstall -h
Windows and macOS specific options:
  -c, --console, --nowindowed
                        Open a console window for standard i/o (default). On Windows this option has no effect if the first script is a '.pyw' file.
  -w, --windowed, --noconsole
                        Windows and macOS: do not provide a console window for standard i/o (__Which means print() will not take effect, so ctypes.windll.user32.MessageBoxW() is used to display GUI messages instead.__). On macOS this also triggers building a macOS .app bundle. On Windows this option is automatically set if the first script is a '.pyw' file. This option is ignored on *NIX systems.
  --hide-console {hide-early,minimize-late,hide-late,minimize-early}
                        Windows only: in console-enabled executable, have bootloader automatically hide or minimize the console window if the program owns the console window (i.e., was not launched from an existing console window).
```

# Other similar tools

(so we no need to call `cmd \k` explicitly for `cmd \k {programpath and argument}`)

1. [invisible.vbs](https://ss64.com/vb/run.html)
```vbs
Dim Args()

ReDim Args(WScript.Arguments.Count - 1)

For i = 0 To WScript.Arguments.Count - 1
   Args(i) = """" & WScript.Arguments(i) & """"
Next

CreateObject("WScript.Shell").Run Join(Args), 0, False

```
An example running 'Demo.cmd' with invisible.vbs
`script.exe "invisible.vbs" "foo.cmd" "bar.cmd"//nologo`

2. [cmdow](https://github.com/ritchielawrence/cmdow)
Cmdow is a win32 console application for manipulating program windows, which is only 86.5 KB. Command example:
`cmdow /run /hid foo.bat arg1 "arg 2"`

Cmdow use .Net Framwork's ShellExecute() function to hide console window, the related code is as follow:
```c#
ParseArgs(argc, argv, &args);

else if(!lstrcmpi("/HID", argv[i])) a->sw_state = SW_HIDE;

RetVal = (int) ShellExecute(NULL, NULL, a->file, a->params, NULL, a->sw_state);

```
However, it seems that using `cmdow /run /hide` **still triggers a brief "splash" cmd window**, which may not behave as expected.

3. [runapp](https://github.com/futurist/runapp)
Runapp dedicates to run windows application using config file, instead of shortcuts, which is only 15.08 KB. Command example:
`Runapp config.arg`

the file config.arg's content is:'
```yaml
:style:hidden
foo.bat
arg1
arg2

```
Runapp hides console window by set process startinfo's `CreateNoWindow` property。
```c#
Process myProcess = new Process();

startInfo.CreateNoWindow = isHide || isFalsy(strWindow);

myProcess.StartInfo = startInfo;

```

4. [Bat To Exe Converter](https://www.f2ko.de/en/applications/bat-to-exe-converter/) by F2ko

   This program supports generating both invisible and invisible exe applications form batch file by GUI operation.

5. [Scoop](https://github.com/ScoopInstaller/Scoop) shim

   > [@cqjjjzr](https://github.com/cqjjjzr) in [kiennq/scoop-better-shimexe#3 (comment)](https://github.com/kiennq/scoop-better-shimexe/pull/3#issue-1185754616) says "a blank console window ... may be suppressed via CREATE_NO_WINDOW creation flag, but I don't know if it would break other things.."
   >
   >
   >
   > Nope, the console window is created as a result of double clicking on the *shim* (which is a console app). The shim can close the console window via `FreeConsole` (which it does) but it can't prevent the OS opening that console window, at least briefly, without being a GUI app (which wouldn't work as a shim for a console app, which is the normal case). [see as.](https://github.com/ScoopInstaller/Scoop/issues/1606#issuecomment-1166297998)

   Scoop use a  `$shim.exe` to call the `target program` with pre-defined arguments, so it has two stages which could introduce console windows:

   1) For every `$shim.exe`,  when creating a shim, Scoop changes **the Subsystem field of the PE header (offset 0x5C)** to ensure the `$shim.exe`  a **GUI applications**, which do not trigger any console window.

```powershell
switch ($SubCommand) {
    'add' {

    $target_subsystem = Get-PESubsystem $resolved_path
            if ($target_subsystem -eq 2) { # we only want to make shims GUI
                Write-Output "Making $shim.exe a GUI binary."
                Set-PESubsystem "$shim.exe" $target_subsystem | Out-Null
            }

    function Get-PESubsystem($filePath) {
            return $binaryReader.ReadInt16()

    function Set-PESubsystem($filePath, $targetSubsystem) {
            $binaryWriter.Write([System.Int16] $targetSubsystem)


```
   ~~2) For  `$target.exe`, when executing program through a shim, Scoop determines whether the `$target.exe` is a console application. If it is a GUI application, which doesn't need the console window triggered by `$shim.exe`  to keep (**It seems this step is no need anymore since the first step exist?**), it manually hides its console using the `FreeConsole()` command.~~

```cpp
int wmain(int argc, wchar_t* argv[])
{

    // Find out if the target program is a console app
    PathUnquoteSpacesW(unquotedPath); //Removes quotes from the beginning and end of a path.

    const auto ret = SHGetFileInfoW(unquotedPath, -1, &sfi, sizeof(sfi), SHGFI_EXETYPE);

    if (ret == 0)
    {
        fprintf(stderr, "Shim: Could not determine if target is a GUI app. Assuming console.\n");
    }

    const auto isWindowsApp = HIWORD(ret) != 0;

    if (isWindowsApp)
    {
        // Unfortunately, this technique will still show a window for a fraction of time,
        // but there's just no workaround.
        FreeConsole();
    }

```

like `runapp`, scoop shim also use a config file named `app.shim` with a entry exe file `app.exe` to package command to an isolated windows execute file, as follow:

- how to create a shim
```bash
# To add a custom shim, use the 'add' subcommand:
scoop shim add <shim_name> <command_path> [<args>...]

# cat.shim's content:
# path = "your_scoop_dir\apps\busybox\current\busybox.exe"
# args = cat

```
```powershell
switch ($SubCommand) {
    'add' {

if ($commandPath -notmatch '[\\/]') {
    $shortPath = $commandPath
    $commandPath = Get-ShimTarget (Get-ShimPath $shortPath $global)
    if (!$commandPath) {
        $exCommand = Get-Command $shortPath -ErrorAction SilentlyContinue
        if ($exCommand -and $exCommand.CommandType -eq 'Application') {
            $commandPath = $exCommand.Path
        } # TODO - add support for more command types: Alias, Cmdlet, ExternalScript, Filter, Function, Script, and Workflow
    }
}

shim $commandPath $global $shimName $commandArgs

function shim($path, $global, $name, $arg) {

    if (!$name) { $name = strip_ext (fname $path) }
    $shim = "$abs_shimdir\$($name.tolower())"

    if ($path -match '\.(exe|com)$') {

        Copy-Item (get_shim_path) "$shim.exe" -Force

        if ($arg) {
            Write-Output "args = $arg" | Out-UTF8File "$shim.shim" -Append
        }

```

- how to run a shim

  see code of [kiennq shim](https://github.com/kiennq/scoop-better-shimexe/blob/43cc946c842f216cce88f00b14a374deba142aa3/shim.cpp#L226)

```cpp
int wmain(int argc, wchar_t* argv[])
{
    auto [path, args] = GetShimInfo();

    // retrieves the command line string
    auto cmd = GetCommandLineW();
    if (cmd[0] == L'\"')
    {
        // when command program enclosed with double quote
        args->append(cmd + wcslen(argv[0]) + 2);
    }
    else
    {
        args->append(cmd + wcslen(argv[0]));
    }

    // Create job object, which can be attached to child processes
    // to make sure they terminate when the parent terminates as well.
    auto [processHandle, threadHandle] = MakeProcess({path, args});

```

- How `MakeProcess()` function works

```cpp
std::tuple<std::unique_handle, std::unique_handle> MakeProcess(ShimInfo const& info)
{
    // Start subprocess
    STARTUPINFOW si = {};
    PROCESS_INFORMATION pi = {};

    auto&& [path, args] = info;
    std::vector<wchar_t> cmd(path->size() + args->size() + 2);
    wmemcpy(cmd.data(), path->c_str(), path->size());
    cmd[path->size()] = L' ';
    wmemcpy(cmd.data() + path->size() + 1, args->c_str(), args->size());
    cmd[path->size() + 1 + args->size()] = L'\0';

    if (CreateProcessW(nullptr, cmd.data(), nullptr, nullptr, TRUE, CREATE_SUSPENDED, nullptr, nullptr, &si, &pi)) // CREATE_NO_WINDOW flag only useful for console application

    else
    {
        if (GetLastError() == ERROR_ELEVATION_REQUIRED)
        {
            // We must elevate the process, which is (basically) impossible with CreateProcess, and therefore we fallback to ShellExecuteEx, which CAN create elevated processes, at the cost of opening a new separate window.

            SHELLEXECUTEINFOW sei = {};
            if (!ShellExecuteExW(&sei))

        else
        {
            fprintf(stderr, "Shim: Could not create process with command '%ls'.\n", cmd.data());
        }
    }

    // Ignore Ctrl-C and other signals
    if (!SetConsoleCtrlHandler(CtrlHandler, TRUE))
    {
        fprintf(stderr, "Shim: Could not set control handler; Ctrl-C behavior may be invalid.\n");
    }

BOOL WINAPI CtrlHandler(DWORD ctrlType)
{
    switch (ctrlType)
    {
    // Ignore all events, and let the child process
    // handle them.

```

Due to that scoop shim deals with arguments from `$target.shim` and `command line` by string concatenate `args->append(cmd + wcslen(argv[0]))`, **scoop shim cannot keep pipe(|), redirect(>) and so many other shell features**.

```cpp
int wmain(int argc, wchar_t* argv[])
{
    auto [path, args] = GetShimInfo();


     // retrieves the command line string
    auto cmd = GetCommandLineW();
    if (cmd[0] == L'\"')
    {
        // when command program enclosed with double quote
        args->append(cmd + wcslen(argv[0]) + 2);
    }
    else
    {
        args->append(cmd + wcslen(argv[0]));
    }

    // Create job object, which can be attached to child processes
    // to make sure they terminate when the parent terminates as well.
    auto [processHandle, threadHandle] = MakeProcess({path, args});

```
appendix scoop shim source code:
```cpp
ShimInfo GetShimInfo()
{
	// #include <windows.h>
    const auto filenameSize = GetModuleFileNameW(nullptr, filename, MAX_PATH);

    // Use filename of current executable to find .shim
    wmemcpy(filename + filenameSize - 3, L"shim", 4U);

    // Read shim
    while (true)
    {
        if (line.substr(0, 4) == L"args")
        {
            args.emplace(line.data() + 7, line.size() - 7 - (line.back() == L'\n' ? 1 : 0));
            continue;
        }
    }
    return {path, NormalizeArgs(args, GetDirectory(filename))};

// replace %~dp0 in .shim with the shim's directory
std::wstring_p NormalizeArgs(std::wstring_p& args, std::wstring_view curDir)
{
    static constexpr auto s_dirPlaceHolder = L"%~dp0"sv;

    auto pos = args->find(s_dirPlaceHolder);
    if (pos != std::wstring::npos)
    {
        args->replace(pos, s_dirPlaceHolder.size(), curDir.data(), curDir.size());
    }

    return args;
}

```

# Notes

This tool is designed for Windows systems and may not work as expected on other operating systems. Additionally, it is important to exercise caution when running commands with this tool, as it can execute commands in the background **without displaying any output or feedback**.

# One more thing

Cause this is the author's first github project, this readme file seems too long for reading. It is recommended to inspect the source code directly which is much more concise and tidier.

