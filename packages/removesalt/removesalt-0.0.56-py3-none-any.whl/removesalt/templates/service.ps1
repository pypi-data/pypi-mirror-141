# &"C:\Program Files\Streambox\Iris\nssm.exe" remove StreamboxIris confirm

try { $service = Get-Service -ErrorAction SilentlyContinue -Name StreamboxIris } catch {}
if (! $service) {
    &"C:\Program Files\Streambox\Iris\nssm.exe" install StreamboxIris "C:\Program Files\Streambox\Iris\decoder.exe"
}
&"C:\Program Files\Streambox\Iris\nssm.exe" set StreamboxIris AppDirectory "C:\Program Files\Streambox\Iris"
&"C:\Program Files\Streambox\Iris\nssm.exe" set StreamboxIris Application "C:\Program Files\Streambox\Iris\decoder.exe"
&"C:\Program Files\Streambox\Iris\nssm.exe" set StreamboxIris AppStdout "C:\ProgramData\Streambox\Iris\log\iris.log"
&"C:\Program Files\Streambox\Iris\nssm.exe" set StreamboxIris AppStderr "C:\ProgramData\Streambox\Iris\log\iris.log"
&"C:\Program Files\Streambox\Iris\nssm.exe" set StreamboxIris Description "Streambox Iris"
&"C:\Program Files\Streambox\Iris\nssm.exe" set StreamboxIris DisplayName "Streambox Iris"
&"C:\Program Files\Streambox\Iris\nssm.exe" set StreamboxIris AppRotateFiles 1
&"C:\Program Files\Streambox\Iris\nssm.exe" set StreamboxIris AppRotateOnline 0
&"C:\Program Files\Streambox\Iris\nssm.exe" set StreamboxIris Start SERVICE_DEMAND_START
&"C:\Program Files\Streambox\Iris\nssm.exe" set StreamboxIris AppRotateSeconds (New-Timespan -Days 1).TotalSeconds
&"C:\Program Files\Streambox\Iris\nssm.exe" set StreamboxIris AppParameters "-xml C:\ProgramData\Streambox\Iris\log\decoder.xml -logfile C:\ProgramData\Streambox\Iris\log\iris.log"
&"C:\Program Files\Streambox\Iris\nssm.exe" set StreamboxIris AppEvents Exit/Post 'C:\Windows\System32\windowspowershell\v1.0\powershell.exe -File ""C:\Program Files\Streambox\Iris\cleanlogs.ps1""'

try { $service = Get-Service -ErrorAction SilentlyContinue -Name StreamboxIris } catch {}
if (!$service) { throw "Can't configure StreamboxIris service" }

# enable all users to start/stop service
&C:\Windows\System32\sc.exe sdset $service "D:AR(A;;CCDCLCSWRPWPDTLOCRSDRCWDWO;;;SY)(A;;CCDCLCSWRPWPDTLOCRSDRCWDWO;;;BA)(A;;CCLCSWLOCRRC;;;IU)(A;;CCLCSWRPWPDTLOCRRC;;;BU)S:(AU;FA;CCDCLCSWRPWPDTLOCRSDRCWDWO;;;WD)"
