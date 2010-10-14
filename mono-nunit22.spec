Name:		mono-nunit22
Version:	2.2.10
Release:	%mkrel 1
Summary:	Unit-testing framework for .NET
URL:		http://www.nunit.org/
License:	MIT with acknowledgement
Group:		Development/Other
Source0:	http://downloads.sourceforge.net/nunit/NUnit-2.2.10-src.zip
Source1:	nunit22.pc
Patch0:		nunit22-mono-2.0.patch
Patch1:		nunit22-key.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	nant
BuildRequires:	unzip
BuildArch: noarch

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
%setup -q -c -n %{name}-%{version}
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
rm -rf $RPM_BUILD_ROOT
cd src/
nant mono-2.0 copy-bins
%{__mkdir_p} $RPM_BUILD_ROOT/%{_datadir}/pkgconfig
cp -p %{S:1} $RPM_BUILD_ROOT/%{_datadir}/pkgconfig
mkdir -p $RPM_BUILD_ROOT/%_prefix/lib/mono/gac/
cd package/NUnit-%{version}
gacutil -i bin/nunit-console.exe -f -package nunit22 -root ${RPM_BUILD_ROOT}/%_prefix/lib
gacutil -i bin/nunit-console-runner.dll -f -package nunit22 -root ${RPM_BUILD_ROOT}/%_prefix/lib
gacutil -i bin/nunit.core.dll -f -package nunit22 -root ${RPM_BUILD_ROOT}/%_prefix/lib
gacutil -i bin/nunit.core.extensions.dll -f -package nunit22 -root ${RPM_BUILD_ROOT}/%_prefix/lib
gacutil -i bin/nunit.framework.dll -f -package nunit22 -root ${RPM_BUILD_ROOT}/%_prefix/lib
gacutil -i bin/nunit.mocks.dll -f -package nunit22 -root ${RPM_BUILD_ROOT}/%_prefix/lib
gacutil -i bin/nunit.util.dll -f -package nunit22 -root ${RPM_BUILD_ROOT}/%_prefix/lib

%clean
rm -rf -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc src/license.rtf
%_prefix/lib/mono/gac/*/
%_prefix/lib/mono/nunit22/

%files devel
%defattr(-,root,root,-)
%{_datadir}/pkgconfig/nunit22.pc


