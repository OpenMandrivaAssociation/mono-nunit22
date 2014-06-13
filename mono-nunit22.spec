Summary:	Unit-testing framework for .NET
Name:		mono-nunit22
Version:	2.2.10
Release:	8
License:	MIT with acknowledgement
Group:		Development/Other
Url:		http://www.nunit.org/
Source0:	http://downloads.sourceforge.net/nunit/NUnit-2.2.10-src.zip
Source1:	nunit22.pc
Patch0:		nunit22-mono-2.0.patch
Patch1:		nunit22-key.patch
BuildArch:	noarch
BuildRequires:	unzip
BuildRequires:	pkgconfig(nant)

%description
NUnit is a unit-testing framework for all .Net languages. Initially ported from
JUnit, this xUnit based unit testing tool is written entirely in C# and has 
been completely redesigned to take advantage of many .NET language features, 
for example custom attributes and other reflection related capabilities. NUnit 
brings xUnit to all .NET languages.

%package devel
Summary:	Unit-testing framework for .NET
Group:		Development/Other
Requires:	%{name} = %{version}-%{release}

%description devel
Development files for mono-nunit22.

%prep
%setup -q -c
%apply_patches

%build
# Use the mono system key instead of generating our own here.
%if %mdvver >= 201100
cp -a /etc/pki/mono/mono.snk nunit.snk
%else
sn -k nunit.snk
%endif
cd src
nant mono-2.0 release build-all

%install
cd src/
nant mono-2.0 copy-bins
mkdir -p %{buildroot}/%{_datadir}/pkgconfig
cp -p %{SOURCE1} %{buildroot}/%{_datadir}/pkgconfig
mkdir -p %{buildroot}/%{_prefix}/lib/mono/gac/
cd package/NUnit-%{version}
gacutil -i bin/nunit-console.exe -f -package nunit22 -root %{buildroot}/%{_prefix}/lib
gacutil -i bin/nunit-console-runner.dll -f -package nunit22 -root %{buildroot}/%{_prefix}/lib
gacutil -i bin/nunit.core.dll -f -package nunit22 -root %{buildroot}/%{_prefix}/lib
gacutil -i bin/nunit.core.extensions.dll -f -package nunit22 -root %{buildroot}/%{_prefix}/lib
gacutil -i bin/nunit.framework.dll -f -package nunit22 -root %{buildroot}/%{_prefix}/lib
gacutil -i bin/nunit.mocks.dll -f -package nunit22 -root %{buildroot}/%{_prefix}/lib
gacutil -i bin/nunit.util.dll -f -package nunit22 -root %{buildroot}/%{_prefix}/lib

%files
%doc src/license.rtf
%{_prefix}/lib/mono/gac/*/
%{_prefix}/lib/mono/nunit22/

%files devel
%{_datadir}/pkgconfig/nunit22.pc

