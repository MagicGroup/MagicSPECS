%define __soversion_major 5
%define __soversion %{__soversion_major}.3

%define with_java 0

Summary: The Berkeley DB database library for C
Name: libdb
Version: 5.3.28
Release: 11%{?dist}
Source0: http://download.oracle.com/berkeley-db/db-%{version}.tar.gz
Source1: http://download.oracle.com/berkeley-db/db.1.85.tar.gz
# For mt19937db.c
Source2: http://www.gnu.org/licenses/lgpl-2.1.txt
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
# License clarification patch
# http://devel.trisquel.info/gitweb/?p=package-helpers.git;a=blob;f=helpers/DATA/db4.8/007-mt19937db.c_license.patch;h=1036db4d337ce4c60984380b89afcaa63b2ef88f;hb=df48d40d3544088338759e8bea2e7f832a564d48
Patch25: 007-mt19937db.c_license.patch
URL: http://www.oracle.com/database/berkeley-db/
License: BSD and LGPLv2 and Sleepycat
Group: System Environment/Libraries
BuildRequires: perl libtool
BuildRequires: tcl-devel >= 8.6
%if 0%{?with_java}
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

%if 0%{?with_java}
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
%endif

%prep
%setup -q -n db-%{version} -a 1
cp %{SOURCE2} .

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
%patch25 -p1 -b .licensefix

cd dist
./s_config
cd ..

%build
CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
CFLAGS="$CFLAGS -DSQLITE_ENABLE_COLUMN_METADATA=1 -DSQLITE_DISABLE_DIRSYNC=1 -DSQLITE_ENABLE_FTS3=3 -DSQLITE_ENABLE_RTREE=1 -DSQLITE_SECURE_DELETE=1 -DSQLITE_ENABLE_UNLOCK_NOTIFY=1 -I../../../lang/sql/sqlite/ext/fts3/"
export CFLAGS

# Build the old db-185 libraries.
make -C db.1.85/PORT/%{_os} OORG="$CFLAGS"

test -d dist/dist-tls || mkdir dist/dist-tls
# Static link db_dump185 with old db-185 libraries.
/bin/sh libtool --tag=CC --mode=compile	%{__cc} $RPM_OPT_FLAGS -Idb.1.85/PORT/%{_os}/include -D_REENTRANT -c util/db_dump185.c -o dist/dist-tls/db_dump185.lo
/bin/sh libtool --tag=LD --mode=link %{__cc} -o dist/dist-tls/db_dump185 dist/dist-tls/db_dump185.lo db.1.85/PORT/%{_os}/libdb.a

# Update config files to understand aarch64
for dir in dist lang/sql/sqlite lang/sql/jdbc lang/sql/odbc; do
  cp /usr/lib/rpm/magic/config.{guess,sub} "$dir"
done

pushd dist/dist-tls
%define _configure ../configure
%configure -C \
	--enable-compat185 --enable-dump185 \
	--enable-shared --enable-static \
	--enable-tcl --with-tcl=%{_libdir} \
	--enable-cxx --enable-sql \
%if 0%{?with_java}
	--enable-java \
%endif
	--enable-test \
	--disable-rpath \
	--with-tcl=%{_libdir}/tcl8.6

# Remove libtool predep_objects and postdep_objects wonkiness so that
# building without -nostdlib doesn't include them twice.  Because we
# already link with g++, weird stuff happens if you don't let the
# compiler handle this.
perl -pi -e 's/^predep_objects=".*$/predep_objects=""/' libtool
perl -pi -e 's/^postdep_objects=".*$/postdep_objects=""/' libtool
perl -pi -e 's/-shared -nostdlib/-shared/' libtool

make %{?_smp_mflags}

%if 0%{?with_java}
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

%makeinstall STRIP=/bin/true -C dist/dist-tls

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

%if 0%{with_java}
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

%if 0%{?with_java}
%post -p /sbin/ldconfig java

%postun -p /sbin/ldconfig java
%endif

%files
%defattr(-,root,root,-)
%doc LICENSE README lgpl-2.1.txt
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
%if 0%{?with_java}
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

%if 0%{?with_java}
%files java
%defattr(-,root,root,-)
%{_libdir}/libdb_java-%{__soversion_major}*.so
%{_datadir}/java/*.jar

%files java-devel
%defattr(-,root,root,-)
%{_libdir}/libdb_java.so
%endif

%changelog
* Mon Nov 09 2015 Liu Di <liudidi@gmail.com> - 5.3.28-11
- 为 Magic 3.0 重建

* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 5.3.28-10
- 为 Magic 3.0 重建

* Mon Jul 14 2014 Liu Di <liudidi@gmail.com> - 5.3.28-9
- 为 Magic 3.0 重建

* Tue May 20 2014 Liu Di <liudidi@gmail.com> - 5.3.28-8
- 为 Magic 3.0 重建

* Tue May 20 2014 Liu Di <liudidi@gmail.com> - 5.3.28-7
- 为 Magic 3.0 重建

* Tue May 20 2014 Liu Di <liudidi@gmail.com> - 5.3.28-6
- 为 Magic 3.0 重建

* Tue May 20 2014 Liu Di <liudidi@gmail.com> - 5.3.28-5
- 为 Magic 3.0 重建

* Sat Feb 22 2014 Peter Robinson <pbrobinson@fedoraproject.org> 5.3.28-4
- Add some of the previous aarch64 bits back as the sub configure don't use the macro

* Sun Jan 26 2014 Peter Robinson <pbrobinson@fedoraproject.org> 5.3.28-3
- Fix configure macro usage for better aarch64 build fix

* Wed Nov 06 2013 Jan Stanek <jstanek@redhat.com> - 5.3.28-2
- Updated config files to allow build on aarch64 (#1022970)

* Tue Oct 08 2013 Jan Stanek <jstanek@redhat.com> - 5.3.28-1
- Added Sleepycat to the license list (#1013841)
- Updated to 5.3.28 (#1013233)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.21-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 28 2013 Tom Callaway <spot@fedoraproject.org> - 5.3.21-12
- add copy of lgpl-2.1.txt

* Thu May 16 2013 Jan Stanek <jstanek@redhat.com> - 5.3.21-11
- Fix missing debuginfo issue for utils subpackage

* Thu May  9 2013 Tom Callaway <spot@fedoraproject.org> - 5.3.21-10
- add license clarification fix

* Wed Apr 03 2013 Jan Stanek <jstanek@redhat.com> 5.3.21-9
- Added sqlite compability CFLAGS (#788496)

* Wed Mar 27 2013 Jan Stanek <jstanek@redhat.com> 5.3.21-8
- Cleaning the specfile - removed gcc-java dependecy other way

* Wed Mar 27 2013 Jan Stanek <jstanek@redhat.com> 5.3.21-7
- Removed dependency on obsolete gcc-java package (#927742)

* Thu Mar  7 2013 Jindrich Novy <jnovy@redhat.com> 5.3.21-6
- add LGPLv2+ and remove Sleepycat in license tag (#886838)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.21-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 27 2012 Tom Callaway <spot@fedoraproject.org> - 5.3.21-4
- fix license tag

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jul 14 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 5.3.21-2
- Specify tag for libtool (fixes FTBFS # 838334 )

* Thu Jul  5 2012 Jindrich Novy <jnovy@redhat.com> 5.3.21-1
- update to 5.3.21
http://download.oracle.com/otndocs/products/berkeleydb/html/changelog_5_3.html

* Tue Jul  3 2012 Jindrich Novy <jnovy@redhat.com> 5.3.15-5
- move C++ header files to cxx-devel

* Tue Jul  3 2012 Jindrich Novy <jnovy@redhat.com> 5.3.15-4
- fix -devel packages dependencies yet more (#832225)

* Sun May  6 2012 Jindrich Novy <jnovy@redhat.com> 5.3.15-3
- package -devel packages correctly

* Sat Apr 21 2012 Jindrich Novy <jnovy@redhat.com> 5.3.15-2
- fix multiarch conflict in libdb-devel (#812901)
- remove unneeded dos2unix BR

* Thu Mar 15 2012 Jindrich Novy <jnovy@redhat.com> 5.3.15-1
- update to 5.3.15
  http://download.oracle.com/otndocs/products/berkeleydb/html/changelog_5_3.html

* Fri Feb 17 2012 Deepak Bhole <dbhole@redhat.com> 5.2.36-5
- Resolves rhbz#794472
- Patch from Omair Majid <omajid@redhat.com> to remove explicit Java 6 req.

* Wed Jan 25 2012 Harald Hoyer <harald@redhat.com> 5.2.36-4
- add filesystem guard

* Wed Jan 25 2012 Harald Hoyer <harald@redhat.com> 5.2.36-3
- install everything in /usr
  https://fedoraproject.org/wiki/Features/UsrMove

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2.36-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jun 15 2011 Jindrich Novy <jnovy@redhat.com> 5.2.36-1
- update to 5.2.36,
  http://download.oracle.com/otndocs/products/berkeleydb/html/changelog_5_2.html#id3647664

* Wed Jun 15 2011 Jindrich Novy <jnovy@redhat.com> 5.2.28-2
- move development documentation to devel-doc subpackage (#705386)

* Tue Jun 14 2011 Jindrich Novy <jnovy@redhat.com> 5.2.28-1
- update to 5.2.28

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Feb  3 2011 Jindrich Novy <jnovy@redhat.com> 5.1.25-1
- update to 5.1.25

* Wed Sep 29 2010 jkeating - 5.1.19-2
- Rebuilt for gcc bug 634757

* Fri Sep 10 2010 Jindrich Novy <jnovy@redhat.com> 5.1.19-1
- update to 5.1.19
- rename -devel-static to -static subpackage (#617800)
- build java on all arches

* Wed Jul  7 2010 Jindrich Novy <jnovy@redhat.com> 5.0.26-1
- update to 5.0.26
- drop BR: ed

* Thu Jun 17 2010 Jindrich Novy <jnovy@redhat.com> 5.0.21-2
- add Requires: libdb-cxx to libdb-devel

* Wed Apr 21 2010 Jindrich Novy <jnovy@redhat.com> 5.0.21-1
- initial build

* Thu Apr 15 2010 Jindrich Novy <jnovy@redhat.com> 5.0.21-0.2
- remove C# documentation
- disable/remove rpath
- fix description
- tighten dependencies
- run ldconfig for cxx and sql subpackages

* Fri Apr  9 2010 Jindrich Novy <jnovy@redhat.com> 5.0.21-0.1
- enable sql
- package 5.0.21
