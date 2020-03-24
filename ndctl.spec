%define major	1
%define mjdax	6
%define libname	%mklibname ndctl %{major}
%define libdax	%mklibname daxctl %{mjdax}
%define devname	%mklibname -d ndctl
%define devdax	%mklibname -d daxctl

Name:		ndctl
Version:	68
Release:	1
Summary:	Manage "libnvdimm" subsystem devices (Non-volatile Memory)
License:	GPLv2
Group:		System/Base
Url:		https://github.com/pmem/ndctl
Source0:	https://github.com/pmem/ndctl/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

Requires:	%{libname} = %{version}-%{release}
Requires:	%{libdax} = %{version}-%{release}
BuildRequires:	autoconf
BuildRequires:	asciidoc
BuildRequires:	xmlto
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	pkgconfig(libkeyutils)
BuildRequires:	pkgconfig(libkmod)
BuildRequires:	pkgconfig(libudev)
BuildRequires:	pkgconfig(uuid)
BuildRequires:	pkgconfig(json-c)
BuildRequires:	pkgconfig(bash-completion)
BuildRequires:	pkgconfig(systemd)

%description
Utility library for managing the "libnvdimm" subsystem.  The "libnvdimm"
subsystem defines a kernel device model and control message interface for
platform NVDIMM resources like those defined by the ACPI 6+ NFIT (NVDIMM
Firmware Interface Table).


%package -n	%{devname}
Summary:	Development files for libndctl
License:	LGPLv2
Group:		Development/Libraries
Requires:	%{libname} = %{EVRD}

%description -n %{devname}
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package -n	daxctl
Summary:	Manage Device-DAX instances
License:	GPLv2
Group:		System Environment/Base
Requires:	%{libdax} = %{version}-%{release}

%description -n daxctl
The daxctl utility provides enumeration and provisioning commands for
the Linux kernel Device-DAX facility. This facility enables DAX mappings
of performance / feature differentiated memory without need of a
filesystem.


%package -n	%{libname}
Summary:	Management library for "libnvdimm" subsystem devices (Non-volatile Memory)
License:	LGPLv2
Group:		System Environment/Libraries
Requires:	%{libdax} = %{version}-%{release}


%description -n %{libname}
Libraries for %{name}.

%package -n 	%{libdax}
Summary:	Management library for "Device DAX" devices
License:	LGPLv2
Group:		System Environment/Libraries

%description -n %{libdax}
Device DAX is a facility for establishing DAX mappings of performance /
feature-differentiated memory. daxctl-libs provides an enumeration /
control API for these devices.

%package -n	%{devdax}
Summary:	Development files for libdaxctl
License:	LGPLv2
Group:		Development/Libraries
Requires:	%{libdax} = %{version}-%{release}

%description -n %{devdax}
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}, a library for enumerating
"Device DAX" devices.  Device DAX is a facility for establishing DAX
mappings of performance / feature-differentiated memory.


%prep
%setup -q ndctl-%{version}

%build
echo %{version} > version
./autogen.sh
%configure --disable-static --disable-silent-rules \
	--disable-docs
%make

%install
%make_install
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%check
make check

%define bashcompdir %(pkg-config --variable=completionsdir bash-completion)
%define udevdir %(pkg-config --variable=udevdir udev)

%files
%license util/COPYING licenses/BSD-MIT licenses/CC0
%{_bindir}/ndctl
#% {_mandir}/man1/ndctl*
%{bashcompdir}/
%{_sysconfdir}/ndctl/monitor.conf
%{_unitdir}/ndctl-monitor.service
%{_sysconfdir}/modprobe.d/nvdimm-security.conf
%{_sysconfdir}/ndctl/keys/keys.readme
%{_datadir}/daxctl/daxctl.conf
#% {_udevrulesdir}/80-ndctl.rules
# % {udevdir}/ndctl-udev

%files -n daxctl
%license util/COPYING licenses/BSD-MIT licenses/CC0
%{_bindir}/daxctl
#% {_mandir}/man1/daxctl*

%files -n %{libname}
%doc README.md
%license COPYING licenses/BSD-MIT licenses/CC0
%{_libdir}/libndctl.so.*

%files -n %{libdax}
%doc README.md
%license COPYING licenses/BSD-MIT licenses/CC0
%{_libdir}/libdaxctl.so.*

%files -n %{devname}
%license COPYING
%{_includedir}/ndctl/
%{_libdir}/libndctl.so
%{_libdir}/pkgconfig/libndctl.pc

%files -n %{devdax}
%license COPYING
%{_includedir}/daxctl/
%{_libdir}/libdaxctl.so
%{_libdir}/pkgconfig/libdaxctl.pc
