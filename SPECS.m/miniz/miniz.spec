%global miniz_revision r4

Name:       miniz
Version:    1.15
Release:    2.%{miniz_revision}%{?dist}
Summary:    Compression library implementing the zlib and Deflate
Group:      System Environment/Libraries
License:    Unlicense
URL:        https://code.google.com/p/%{name}/
Source0:    https://%{name}.googlecode.com/files/%{name}_v%(echo '%{version}' | tr -d .)_%{miniz_revision}.7z
BuildRequires:  p7zip

%description
Miniz is a lossless, high performance data compression library in a single
source file that implements the zlib (RFC 1950) and Deflate (RFC 1951)
compressed data format specification standards. It supports the most commonly
used functions exported by the zlib library, but is a completely independent
implementation so zlib's licensing requirements do not apply. It also
contains simple to use functions for writing PNG format image files and
reading/writing/appending ZIP format archives. Miniz's compression speed has
been tuned to be comparable to zlib's, and it also has a specialized real-time
compressor function designed to compare well against fastlz/minilzo.

%package devel
Group:      Development/Libraries
Summary:    Development files for the %{name} library
Requires:   %{name}%{?_isa} = %{version}-%{release}
Requires:   glibc-headers%{?_isa}

%description devel
Header files for developing applications that use the %{name} library.


%prep
%setup -c -T -n %{name}-%{version}_%{miniz_revision}
7za e '%{SOURCE0}'
# Remove prebuilt executables
find -name '*.exe' -exec rm -- {} +
# Extract a header file
sed -e '/End of Header/q' < %{name}.c > %{name}.h
# Prepare test for linking against the library
sed -i -e 's/#include "miniz.c"/#include <miniz.h>/' miniz_tester.cpp

%global soname lib%{name}.so.0.1

%build
# Upstream CMakeLists.txt does not produce a library, build it.
# Inject downstream SONAME, bug #1152653
gcc %{optflags} -fPIC -DPIC -D_LARGEFILE64_SOURCE=1 -D_FILE_OFFSET_BITS=64 \
    -fno-strict-aliasing %{name}.c -c -o %{name}.o
gcc %{?__global_ldflags} -fPIC -shared -Wl,-soname,%{soname} \
    %{name}.o -o %{soname}
ln -s %{soname} lib%{name}.so
# Build test against the library
g++ %{optflags} -D_LARGEFILE64_SOURCE=1 -D_FILE_OFFSET_BITS=64 \
    -I. miniz_tester.cpp -c -o miniz_tester.o
g++ %{optflags} -D_LARGEFILE64_SOURCE=1 -D_FILE_OFFSET_BITS=64 \
    -I. timer.cpp -c -o timer.o
g++ %{?__global_ldflags} -L. -l%{name} miniz_tester.o timer.o -o miniz_tester

%check
LD_LIBRARY_PATH=$PWD ./miniz_tester

%install
install -d '%{buildroot}/%{_libdir}'
install %{soname} '%{buildroot}/%{_libdir}'
ln -s %{soname} '%{buildroot}/%{_libdir}/lib%{name}.so'
install -d '%{buildroot}/%{_includedir}'
install -m 0644 %{name}.h '%{buildroot}/%{_includedir}'

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_libdir}/%{soname}

%files devel
%{_includedir}/%{name}.h
%{_libdir}/lib%{name}.so


%changelog
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-2.r4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Oct 14 2014 Petr Pisar <ppisar@redhat.com> - 1.15-1.r4
- 1.15r4 version packaged


