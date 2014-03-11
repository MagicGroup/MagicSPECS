%define __soversion_major 5
%define __soversion %{__soversion_major}.3

%define WITH_JAVA 0

Summary: The Berkeley DB database library for C
Name: libdb
Version: 5.3.21
Release: 4%{?dist}
Source0: http://download.oracle.com/berkeley-db/db-%{version}.tar.gz
Source1: http://download.oracle.com/berkeley-db/db.1.85.tar.gz
Patch0: libdb-multiarch.patch
# db-1.85 upstream patches
Patch10: http://www.oracle.com/technology/products/berkeley-db/db/update/1.85/patch.1.1
Patch11: http://www.oracle.com/technology/products/berkeley-db/db/update/1.85/patch.1.2
Patch12: http://www.oracle.com/technology/products/berkeley-db/db/update/1.85/patch.1.3
Patch13: http://www.oracle.com/technology/products/berkeley-db/db/update/1.85/patch.1.4
# other patches
Patch20: db-1.85-errno.patch
Patch22: db-4.6.21-1.85-compat.patch
Patch24: db-4.5.20-jni-include-dir.patch
URL: http://www.oracle.com/database/berkeley-db/
License: BSD
Group: System Environment/Libraries
BuildRequires: perl libtool
BuildRequires: tcl-devel >= 8.5.2-3
%if 0%{?WITH_JAVA}
BuildRequires: gcc-java
BuildRequires: java-devel >= 1:1.6.0
%endif
BuildRequires: chrpath
Conflicts: filesystem < 3

%description
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. The Berkeley DB includes B+tree, Extended
Linear Hashing, Fixed and Variable-length record access methods,
transactions, locking, logging, shared memory caching, and database
recovery. The Berkeley DB supports C, C++, Java, and Perl APIs. It is
used by many applications, including Python and Perl, so this should
be installed on all systems.

%package utils
Summary: Command line tools for managing Berkeley DB databases
Group: Applications/Databases
Requires: %{name}%{?_isa} = %{version}-%{release}

%description utils
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. Berkeley DB includes B+tree, Extended
Linear Hashing, Fixed and Variable-length record access methods,
transactions, locking, logging, shared memory caching, and database
recovery. DB supports C, C++, Java and Perl APIs.

%package devel
Summary: C development files for the Berkeley DB library
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. This package contains the header files,
libraries, and documentation for building programs which use the
Berkeley DB.

%package devel-doc
Summary: C development documentation files for the Berkeley DB library
Group: Documentation
Requires: %{name} = %{version}-%{release}
Requires: %{name}-devel = %{version}-%{release}
BuildArch: noarch

%description devel-doc
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. This package contains the header files,
libraries, and documentation for building programs which use the
Berkeley DB.

%package devel-static
Summary: Berkeley DB static libraries
Group: Development/Libraries
Requires: %{name}-devel%{?_isa} = %{version}-%{release}

%description devel-static
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. This package contains static libraries
needed for applications that require static linking of
Berkeley DB.

%package cxx
Summary: The Berkeley DB database library for C++
Group: System Environment/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description cxx
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. The Berkeley DB includes B+tree, Extended
Linear Hashing, Fixed and Variable-length record access methods,
transactions, locking, logging, shared memory caching, and database
recovery. The Berkeley DB supports C, C++, Java, and Perl APIs. It is
used by many applications, including Python and Perl, so this should
be installed on all systems.

%package cxx-devel
Summary: The Berkeley DB database library for C++
Group: System Environment/Libraries
Requires: %{name}-cxx%{?_isa} = %{version}-%{release}
Requires: %{name}-devel%{?_isa} = %{version}-%{release}

%description cxx-devel
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. The Berkeley DB includes B+tree, Extended
Linear Hashing, Fixed and Variable-length record access methods,
transactions, locking, logging, shared memory caching, and database
recovery. The Berkeley DB supports C, C++, Java, and Perl APIs. It is
used by many applications, including Python and Perl, so this should
be installed on all systems.

%package tcl
Summary: Development files for using the Berkeley DB with tcl
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description tcl
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. This package contains the libraries
for building programs which use the Berkeley DB in Tcl.

%package tcl-devel
Summary: Development files for using the Berkeley DB with tcl
Group: Development/Libraries
Requires: %{name}-tcl%{?_isa} = %{version}-%{release}

%description tcl-devel
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. This package contains the libraries
for building programs which use the Berkeley DB in Tcl.

%package sql
Summary: Development files for using the Berkeley DB with sql
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description sql
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. This package contains the libraries
for building programs which use the Berkeley DB in SQL.

%package sql-devel
Summary: Development files for using the Berkeley DB with sql
Group: Development/Libraries
Requires: %{name}-sql%{?_isa} = %{version}-%{release}

%description sql-devel
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. This package contains the libraries
for building programs which use the Berkeley DB in SQL.

%package java
Summary: Development files for using the Berkeley DB with Java
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description java
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. This package contains the libraries
for building programs which use the Berkeley DB in Java.

%package java-devel
Summary: Development files for using the Berkeley DB with Java
Group: Development/Libraries
Requires: %{name}-java%{?_isa} = %{version}-%{release}

%description java-devel
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. This package contains the libraries
for building programs which use the Berkeley DB in Java.

%prep
%setup -q -n db-%{version} -a 1

%patch0 -p1 -b .multiarch
pushd db.1.85/PORT/linux
%patch10 -p0 -b .1.1
popd
pushd db.1.85
%patch11 -p0 -b .1.2
%patch12 -p0 -b .1.3
%patch13 -p0 -b .1.4
%patch20 -p1 -b .errno
popd

%patch22 -p1 -b .185compat
%patch24 -p1 -b .4.5.20.jni

cd dist
./s_config

%build
export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"

# Build the old db-185 libraries.
make -C db.1.85/PORT/%{_os} OORG="$CFLAGS"

test -d dist/dist-tls || mkdir dist/dist-tls
# Static link db_dump185 with old db-185 libraries.
/usr/bin/sh libtool --tag=CC --mode=compile	%{__cc} $RPM_OPT_FLAGS -Idb.1.85/PORT/%{_os}/include -D_REENTRANT -c util/db_dump185.c -o dist/dist-tls/db_dump185.lo
/usr/bin/sh libtool --tag=LD --mode=link %{__cc} -o dist/dist-tls/db_dump185 dist/dist-tls/db_dump185.lo db.1.85/PORT/%{_os}/libdb.a

pushd dist/dist-tls
ln -sf ../configure .
%configure -C \
	--enable-compat185 --enable-dump185 \
	--enable-shared --enable-static \
	--enable-tcl --with-tcl=%{_libdir} \
	--enable-cxx --enable-sql \
%if 0%{?WITH_JAVA}
	--enable-java \
%else
	--disable-java \
%endif
	--enable-test \
	--disable-rpath \
	--with-tcl=%{_libdir}/tcl8.5

# Remove libtool predep_objects and postdep_objects wonkiness so that
# building without -nostdlib doesn't include them twice.  Because we
# already link with g++, weird stuff happens if you don't let the
# compiler handle this.
perl -pi -e 's/^predep_objects=".*$/predep_objects=""/' libtool
perl -pi -e 's/^postdep_objects=".*$/postdep_objects=""/' libtool
perl -pi -e 's/-shared -nostdlib/-shared/' libtool

make %{?_smp_mflags}

%if 0%{WITH_JAVA}
# XXX hack around libtool not creating ./libs/libdb_java-X.Y.lai
LDBJ=./.libs/libdb_java-%{__soversion}.la
if test -f ${LDBJ} -a ! -f ${LDBJ}i; then
	sed -e 's,^installed=no,installed=yes,' < ${LDBJ} > ${LDBJ}i
fi
%endif
popd

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_includedir}
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}

%makeinstall -C dist/dist-tls

# XXX Nuke non-versioned archives and symlinks
rm -f ${RPM_BUILD_ROOT}%{_libdir}/{libdb.a,libdb_cxx.a,libdb_tcl.a,libdb_sql.a}

chmod +x ${RPM_BUILD_ROOT}%{_libdir}/*.so*

# Move the header files to a subdirectory, in case we're deploying on a
# system with multiple versions of DB installed.
mkdir -p ${RPM_BUILD_ROOT}%{_includedir}/%{name}
mv ${RPM_BUILD_ROOT}%{_includedir}/*.h ${RPM_BUILD_ROOT}%{_includedir}/%{name}/

# Create symlinks to includes so that "use <db.h> and link with -ldb" works.
for i in db.h db_cxx.h db_185.h; do
	ln -s %{name}/$i ${RPM_BUILD_ROOT}%{_includedir}
done

%if 0%{WITH_JAVA}
# Move java jar file to the correct place
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/java
mv ${RPM_BUILD_ROOT}%{_libdir}/*.jar ${RPM_BUILD_ROOT}%{_datadir}/java
%endif

# Eliminate installed doco
rm -rf ${RPM_BUILD_ROOT}%{_prefix}/docs

# XXX Avoid Permission denied. strip when building as non-root.
chmod u+w ${RPM_BUILD_ROOT}%{_bindir} ${RPM_BUILD_ROOT}%{_bindir}/*

# remove unneeded .la files (#225675)
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la

# remove RPATHs
chrpath -d ${RPM_BUILD_ROOT}%{_libdir}/*.so ${RPM_BUILD_ROOT}%{_bindir}/*

# unify documentation and examples, remove stuff we don't need
rm -rf docs/csharp
rm -rf examples/csharp
rm -rf docs/installation
mv examples docs
magic_rpm_clean.sh

%clean
rm -rf ${RPM_BUILD_ROOT}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post -p /sbin/ldconfig cxx

%postun -p /sbin/ldconfig cxx

%post -p /sbin/ldconfig sql

%postun -p /sbin/ldconfig sql

%post -p /sbin/ldconfig tcl

%postun -p /sbin/ldconfig tcl

%if 0%{WITH_JAVA}
%post -p /sbin/ldconfig java

%postun -p /sbin/ldconfig java
%endif

%files
%defattr(-,root,root,-)
%doc LICENSE README
%{_libdir}/libdb-%{__soversion}.so
%{_libdir}/libdb-%{__soversion_major}.so

%files devel
%defattr(-,root,root,-)
%{_libdir}/libdb.so
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/db.h
%{_includedir}/%{name}/db_185.h
%{_includedir}/db.h
%{_includedir}/db_185.h

%files devel-doc
%defattr(-,root,root,-)
%doc	docs/*

%files devel-static
%defattr(-,root,root,-)
%{_libdir}/libdb-%{__soversion}.a
%{_libdir}/libdb_cxx-%{__soversion}.a
%{_libdir}/libdb_tcl-%{__soversion}.a
%{_libdir}/libdb_sql-%{__soversion}.a
%if 0%{WITH_JAVA}
%{_libdir}/libdb_java-%{__soversion}.a
%endif

%files utils
%defattr(-,root,root,-)
%{_bindir}/db*_archive
%{_bindir}/db*_checkpoint
%{_bindir}/db*_deadlock
%{_bindir}/db*_dump*
%{_bindir}/db*_hotbackup
%{_bindir}/db*_load
%{_bindir}/db*_printlog
%{_bindir}/db*_recover
%{_bindir}/db*_replicate
%{_bindir}/db*_stat
%{_bindir}/db*_upgrade
%{_bindir}/db*_verify
%{_bindir}/db*_tuner

%files cxx
%defattr(-,root,root,-)
%{_libdir}/libdb_cxx-%{__soversion}.so
%{_libdir}/libdb_cxx-%{__soversion_major}.so

%files cxx-devel
%defattr(-,root,root,-)
%{_includedir}/%{name}/db_cxx.h
%{_includedir}/db_cxx.h
%{_libdir}/libdb_cxx.so

%files tcl
%defattr(-,root,root,-)
%{_libdir}/libdb_tcl-%{__soversion}.so
%{_libdir}/libdb_tcl-%{__soversion_major}.so

%files tcl-devel
%defattr(-,root,root,-)
%{_libdir}/libdb_tcl.so

%files sql
%defattr(-,root,root,-)
%{_libdir}/libdb_sql-%{__soversion}.so
%{_libdir}/libdb_sql-%{__soversion_major}.so

%files sql-devel
%defattr(-,root,root,-)
%{_bindir}/dbsql
%{_libdir}/libdb_sql.so
%{_includedir}/%{name}/dbsql.h

%if 0%{WITH_JAVA}
%files java
%defattr(-,root,root,-)
%{_libdir}/libdb_java-%{__soversion_major}*.so
%{_datadir}/java/*.jar

%files java-devel
%defattr(-,root,root,-)
%{_libdir}/libdb_java.so
%endif

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 5.3.21-4
- 为 Magic 3.0 重建


