%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}


Name:           libdmtx
Version:        0.7.2
Release:        11%{?dist}
Summary:        Library for working with Data Matrix 2D bar-codes

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://www.libdmtx.org/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
Patch0:         %{name}-0.7.2-php54.patch
Patch1:         %{name}-0.7.2-ruby19.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  ImageMagick-devel
# required for tests
BuildRequires:  SDL_image-devel
BuildRequires:  libGLU-devel
BuildRequires:  libpng-devel
# language bindings
BuildRequires:  php-devel
BuildRequires:  python-devel
BuildRequires:  ruby
BuildRequires:  ruby-devel
#BuildRequires:  java-1.6.0-devel


%description
libdmtx is open source software for reading and writing Data Matrix 2D
bar-codes on Linux, Unix, OS X, Windows, and mobile devices. At its core
libdmtx is a shared library, allowing C/C++ programs to use its capabilities
without restrictions or overhead.

The included utility programs, dmtxread and dmtxwrite, provide the official
interface to libdmtx from the command line, and also serve as a good reference
for programmers who wish to write their own programs that interact with
libdmtx. All of the software in the libdmtx package is distributed under
the LGPLv2 and can be used freely under these terms.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        utils
Summary:        Utilities for %{name}
Group:          Applications/System
Requires:       %{name} = %{version}-%{release}

%description    utils
The %{name}-utils package contains utilities that use %{name}.

# language bindings
%package -n     php-libdmtx
Summary:        PHP bindings for %{name}
Group:          System Environment/Libraries
License:        GPLv2+
Requires:       %{name} = %{version}-%{release}
Requires:       php-common

%description -n php-libdmtx
The php-%{name} package contains bindings for using %{name} from PHP.

%package -n     python-libdmtx
Summary:        Python bindings for %{name}
Group:          System Environment/Libraries
Requires:       %{name} = %{version}-%{release}

%description -n python-libdmtx
The python-%{name} package contains bindings for using %{name} from Python.

%package -n     ruby-libdmtx
Summary:        Ruby bindings for %{name}
Group:          System Environment/Libraries
Requires:       %{name} = %{version}-%{release}
Provides:       ruby(%{name}) = %{version}

%description -n ruby-libdmtx
The ruby-%{name} package contains bindings for using %{name} from Ruby.


%prep
%setup -q
%patch0 -p1 -b .php54
%patch1 -p1 -b .ruby19

# fix permissions
chmod a-x wrapper/{php,python}/README


%build
%configure --disable-static
make %{?_smp_mflags}

# temporary installation required by the language wrappers
make install DESTDIR=/tmp

# language wrappers must be built separately
pushd wrapper
pushd php
phpize
%configure --disable-static

# Don't use rpath!
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make EXTRA_CFLAGS="-I/tmp%{_includedir}" DMTX_SHARED_LIBADD="-L/tmp%{_libdir} -ldmtx"
popd

pushd python
# fix paths
sed -i.orig -e "s|/usr/local/include|/tmp%{_includedir}|" -e "s|/usr/local/lib|/tmp%{_libdir}|" setup.py
python setup.py build
chmod 0755 build/lib.*/*.so
popd

pushd ruby
ruby extconf.rb --vendor
make CPPFLAGS="-I/tmp%{_includedir}" LIBPATH="-L/tmp%{_libdir} -ldmtx"
popd

#pushd java
#make LIBDMTX_LA="/tmp%{_libdir}/libdmtx.so"
#popd
popd


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

pushd wrapper
pushd php
make install INSTALL_ROOT=$RPM_BUILD_ROOT
popd

pushd python
python setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
popd

pushd ruby
# ruby_headers= used as a workaround:
# https://bugzilla.redhat.com/show_bug.cgi?id=921650
make install DESTDIR=$RPM_BUILD_ROOT ruby_headers=
popd

#pushd java
#popd
popd


%check
make check
pushd test
for t in simple unit
do
    ./${t}_test/${t}_test
done
popd


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING.LESSER ChangeLog KNOWNBUG NEWS README README.linux TODO
%{_libdir}/%{name}.so.*

%files devel
%defattr(-,root,root,-)
%doc
%{_includedir}/*
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_mandir}/man3/%{name}.3*

%files utils
%defattr(-,root,root,-)
%{_bindir}/dmtx*
%{_mandir}/man1/dmtx*.1*

%files -n php-libdmtx
%defattr(-,root,root,-)
%doc COPYING wrapper/php/README
%{_libdir}/php/modules/*.so

%files -n python-libdmtx
%defattr(-,root,root,-)
%doc wrapper/python/README
%{python_sitearch}/*

%files -n ruby-libdmtx
%defattr(-,root,root,-)
%doc wrapper/ruby/README
%{ruby_vendorarchdir}/*.so


%changelog
* Sun Jun 22 2014 Liu Di <liudidi@gmail.com> - 0.7.2-11
- 为 Magic 3.0 重建

* Tue Mar 19 2013 Vít Ondruch <vondruch@redhat.com> - 0.7.2-10
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Mar 04 2012 Dan Horák <dan[at]danny.cz> - 0.7.2-7
- rebuilt for ImageMagick soname bump

* Wed Feb 08 2012 Dan Horák <dan[at]danny.cz> - 0.7.2-6
- fix build with php 5.4 and ruby 1.9.3

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov 17 2010 Dan Horák <dan[at]danny.cz> 0.7.2-3
- updated license for the php subpackage
- run few tests

* Sat May 29 2010 Dan Horák <dan[at]danny.cz> 0.7.2-2
- added language bindigs

* Wed Feb  3 2010 Dan Horák <dan[at]danny.cz> 0.7.2-1
- initial Fedora version
