# the set of arches on which libgcj provides gcj and libgcj-javac-placeholder.sh
%define java_arches %{ix86} alpha ia64 ppc sparc sparcv9 x86_64 s390 s390x
# %define java_arches alpha ia64 ppc sparc sparcv9 x86_64 s390 s390x
%define __soversion 4.8

Summary: The Berkeley DB database library (version 4) for C
Summary(zh_CN.UTF-8): C 语言的 Berkeley DB 数据库库(版本 4)
Name: db4
Version: 4.8.30
Release: 4%{?dist}
Source0: http://download.oracle.com/berkeley-db/db-%{version}.tar.gz
Source1: http://download.oracle.com/berkeley-db/db.1.85.tar.gz
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
Group(zh_CN.UTF-8): 系统环境/库
# unversioned obsoletes are OK here as these BDB versions never occur again
Obsoletes: db1, db2, db3
BuildRequires: perl, libtool, ed, util-linux-ng
BuildRequires: tcl-devel >= 8.5.2-3
%ifarch %{java_arches}
BuildRequires: gcc-java
# BuildRequires: java-1.6.0-openjdk-devel
%endif
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. The Berkeley DB includes B+tree, Extended
Linear Hashing, Fixed and Variable-length record access methods,
transactions, locking, logging, shared memory caching, and database
recovery. The Berkeley DB supports C, C++, Java, and Perl APIs. It is
used by many applications, including Python and Perl, so this should
be installed on all systems.

%description -l zh_CN.UTF-8
Berkeley 数据库 (Berkeley DB) 是一个编程工具包。它为传统的和客户机/服务
器程序提供嵌入的数据库支持。Berkeley DB 包括 B+tree、扩展的线形散列、固
定的和长短不同的记录存取方法、事务、上锁、记录日志、共享的内存缓存、以
及数据库恢复。Berkeley DB 支持 C、C++、Java、和 Perl API。它被许多程序
使用，包括 Python 和 Perl，因此它应该在所有系统上安装。

%package cxx
Summary: The Berkeley DB database library (version 4) for C++
Summary(zh_CN.UTF-8): C++ 语言的 Berkeley DB 数据库库(版本 4)
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库

%description cxx
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. The Berkeley DB includes B+tree, Extended
Linear Hashing, Fixed and Variable-length record access methods,
transactions, locking, logging, shared memory caching, and database
recovery. The Berkeley DB supports C, C++, Java, and Perl APIs. It is
used by many applications, including Python and Perl, so this should
be installed on all systems.

%description cxx -l zh_CN.UTF-8
Berkeley 数据库 (Berkeley DB) 是一个编程工具包。它为传统的和客户机/服务
器程序提供嵌入的数据库支持。Berkeley DB 包括 B+tree、扩展的线形散列、固
定的和长短不同的记录存取方法、事务、上锁、记录日志、共享的内存缓存、以
及数据库恢复。Berkeley DB 支持 C、C++、Java、和 Perl API。它被许多程序
使用，包括 Python 和 Perl，因此它应该在所有系统上安装。

%package utils
Summary: Command line tools for managing Berkeley DB (version 4) databases
Summary(zh_CN.UTF-8): 管理 Berkeley DB (版本 4) 数据库的命令行工具
Group: Applications/Databases
Group(zh_CN.UTF-8): 应用程序/数据库
Requires: db4 = %{version}-%{release}
Obsoletes: db1-utils, db2-utils, db3-utils

%description utils
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. Berkeley DB includes B+tree, Extended
Linear Hashing, Fixed and Variable-length record access methods,
transactions, locking, logging, shared memory caching, and database
recovery. DB supports C, C++, Java and Perl APIs.

%description utils -l zh_CN.UTF-8
Berkeley 数据库 (Berkeley DB) 是一个编程工具包。它为传统的和客户机/服务
器程序提供嵌入的数据库支持。Berkeley DB 包括 B+tree、扩展的线形散列、固
定的和长短不同的记录存取方法、事务、上锁、记录日志、共享的内存缓存、以
及数据库恢复。Berkeley DB 支持 C、C++、Java、和 Perl API。它被许多程序
使用，包括 Python 和 Perl，因此它应该在所有系统上安装。

%package devel
Summary: C development files for the Berkeley DB (version 4) library
Summary(zh_CN.UTF-8): Berkeley DB (版本 4) 库的 C 开发文件
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: db4 = %{version}-%{release}
Requires: db4-cxx = %{version}-%{release}
Obsoletes: db1-devel, db2-devel, db3-devel

%description devel
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. This package contains the header files,
libraries, and documentation for building programs which use the
Berkeley DB.

%description devel -l zh_CN.UTF-8
Berkeley 数据库 (Berkeley DB) 是一个编程工具包。它为传统的和客户机/服务
器程序提供嵌入的数据库支持。Berkeley DB 包括 B+tree、扩展的线形散列、固
定的和长短不同的记录存取方法、事务、上锁、记录日志、共享的内存缓存、以
及数据库恢复。Berkeley DB 支持 C、C++、Java、和 Perl API。它被许多程序
使用，包括 Python 和 Perl，因此它应该在所有系统上安装。

%package devel-static
Summary: Berkeley DB (version 4) static libraries
Summary(zh_CN.UTF-8): Berkeley DB (版本 4) 静态库
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: db4-devel = %{version}-%{release}

%description devel-static
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. This package contains static libraries
needed for applications that require statical linking of
Berkeley DB.

%description devel-static -l zh_CN.UTF-8
Berkeley 数据库 (Berkeley DB) 是一个编程工具包。它为传统的和客户机/服务
器程序提供嵌入的数据库支持。Berkeley DB 包括 B+tree、扩展的线形散列、固
定的和长短不同的记录存取方法、事务、上锁、记录日志、共享的内存缓存、以
及数据库恢复。Berkeley DB 支持 C、C++、Java、和 Perl API。它被许多程序
使用，包括 Python 和 Perl，因此它应该在所有系统上安装。

%package tcl
Summary: Development files for using the Berkeley DB (version 4) with tcl
Summary(zh_CN.UTF-8): Berykeley DB (版本 4) 的 Tcl 开发文件
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}

%description tcl
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. This package contains the libraries
for building programs which use the Berkeley DB in Tcl.

%description tcl -l zh_CN.UTF-8
Berkeley 数据库 (Berkeley DB) 是一个编程工具包。它为传统的和客户机/服务
器程序提供嵌入的数据库支持。Berkeley DB 包括 B+tree、扩展的线形散列、固
定的和长短不同的记录存取方法、事务、上锁、记录日志、共享的内存缓存、以
及数据库恢复。Berkeley DB 支持 C、C++、Java、和 Perl API。它被许多程序
使用，包括 Python 和 Perl，因此它应该在所有系统上安装。

%package java
Summary: Development files for using the Berkeley DB (version 4) with Java
Summary(zh_CN.UTF-8): Berykeley DB (版本 4) 的 Java 开发文件
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}

%description java
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. This package contains the libraries
for building programs which use the Berkeley DB in Java.

%description tcl -l zh_CN.UTF-8
Berkeley 数据库 (Berkeley DB) 是一个编程工具包。它为传统的和客户机/服务
器程序提供嵌入的数据库支持。Berkeley DB 包括 B+tree、扩展的线形散列、固
定的和长短不同的记录存取方法、事务、上锁、记录日志、共享的内存缓存、以
及数据库恢复。Berkeley DB 支持 C、C++、Java、和 Perl API。它被许多程序
使用，包括 Python 和 Perl，因此它应该在所有系统上安装。

%prep
%setup -q -n db-%{version} -a 1

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

# Remove tags files which we don't need.
find . -name tags | xargs rm -f
# Define a shell function for fixing HREF references in the docs, which
# would otherwise break when we split the docs up into subpackages.
fixup_href() {
	for doc in $@ ; do
		chmod u+w ${doc}
		sed	-e 's,="../api_c/,="../../%{name}-devel-%{version}/api_c/,g' \
			-e 's,="api_c/,="../%{name}-devel-%{version}/api_c/,g' \
			-e 's,="../api_cxx/,="../../%{name}-devel-%{version}/api_cxx/,g' \
			-e 's,="api_cxx/,="../%{name}-devel-%{version}/api_cxx/,g' \
			-e 's,="../api_tcl/,="../../%{name}-devel-%{version}/api_tcl/,g' \
			-e 's,="api_tcl/,="../%{name}-devel-%{version}/api_tcl/,g' \
			-e 's,="../java/,="../../%{name}-devel-%{version}/java/,g' \
			-e 's,="java/,="../%{name}-devel-%{version}/java/,g' \
			-e 's,="../examples_c/,="../../%{name}-devel-%{version}/examples_c/,g' \
			-e 's,="examples_c/,="../%{name}-devel-%{version}/examples_c/,g' \
			-e 's,="../examples_cxx/,="../../%{name}-devel-%{version}/examples_cxx/,g' \
			-e 's,="examples_cxx/,="../%{name}-devel-%{version}/examples_cxx/,g' \
			-e 's,="../ref/,="../../%{name}-devel-%{version}/ref/,g' \
			-e 's,="ref/,="../%{name}-devel-%{version}/ref/,g' \
			-e 's,="../images/,="../../%{name}-devel-%{version}/images/,g' \
			-e 's,="images/,="../%{name}-devel-%{version}/images/,g' \
			-e 's,="../utility/,="../../%{name}-utils-%{version}/utility/,g' \
			-e 's,="utility/,="../%{name}-utils-%{version}/utility/,g' ${doc} > ${doc}.new
		touch -r ${doc} ${doc}.new
		cat ${doc}.new > ${doc}
		touch -r ${doc}.new ${doc}
		rm -f ${doc}.new
	done
}

set +x
# Fix all of the HTML files.
fixup_href `find . -name "*.html"`
set -x

cd dist
./s_config

%build
CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"; export CFLAGS

# Build the old db-185 libraries.
make -C db.1.85/PORT/%{_os} OORG="$CFLAGS"

build() {
	test -d dist/$1 || mkdir dist/$1
	# Static link db_dump185 with old db-185 libraries.
	/bin/sh libtool --mode=compile	%{__cc} $RPM_OPT_FLAGS -Idb.1.85/PORT/%{_os}/include -D_REENTRANT -c db_dump185/db_dump185.c -o dist/$1/db_dump185.lo
	/bin/sh libtool --mode=link	%{__cc} -o dist/$1/db_dump185 dist/$1/db_dump185.lo db.1.85/PORT/%{_os}/libdb.a

	pushd dist
	popd
	pushd dist/$1
	ln -sf ../configure .
	# XXX --enable-diagnostic should be disabled for production (but is
	# useful).
	# XXX --enable-debug_{r,w}op should be disabled for production.
	%configure -C \
		--enable-compat185 --enable-dump185 \
		--enable-shared --enable-static \
		--enable-tcl --with-tcl=%{_libdir} \
		--enable-cxx \
%ifarch %{java_arches}
		--enable-java \
%else
		--disable-java \
%endif
		--enable-test \
		--with-tcl=%{_libdir}/tcl8.5 \
		# --enable-diagnostic \
		# --enable-debug --enable-debug_rop --enable-debug_wop \

	# Remove libtool predep_objects and postdep_objects wonkiness so that
	# building without -nostdlib doesn't include them twice.  Because we
	# already link with g++, weird stuff happens if you don't let the
	# compiler handle this.
	perl -pi -e 's/^predep_objects=".*$/predep_objects=""/' libtool
	perl -pi -e 's/^postdep_objects=".*$/postdep_objects=""/' libtool
	perl -pi -e 's/-shared -nostdlib/-shared/' libtool

	make %{?_smp_mflags}

	# XXX hack around libtool not creating ./libs/libdb_java-X.Y.lai
	LDBJ=./.libs/libdb_java-%{__soversion}.la
	if test -f ${LDBJ} -a ! -f ${LDBJ}i; then
		sed -e 's,^installed=no,installed=yes,' < ${LDBJ} > ${LDBJ}i
	fi

	popd
}

build dist-tls

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_includedir}
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}

%makeinstall -C dist/dist-tls

# XXX Nuke non-versioned archives and symlinks
rm -f ${RPM_BUILD_ROOT}%{_libdir}/{libdb.a,libdb_cxx.a}
rm -f ${RPM_BUILD_ROOT}%{_libdir}/libdb-4.so
rm -f ${RPM_BUILD_ROOT}%{_libdir}/libdb_cxx-4.so
rm -f ${RPM_BUILD_ROOT}%{_libdir}/libdb_tcl-4.so
rm -f ${RPM_BUILD_ROOT}%{_libdir}/libdb_tcl.so

chmod +x ${RPM_BUILD_ROOT}%{_libdir}/*.so*

# Move the main shared library from /usr/lib* to /lib* directory.
if [ "%{_libdir}" != "/%{_lib}" ]; then
  mkdir -p $RPM_BUILD_ROOT/%{_lib}/
  mv $RPM_BUILD_ROOT/%{_libdir}/libdb-%{__soversion}.so $RPM_BUILD_ROOT/%{_lib}/

# Leave relative symlinks in %{_libdir}.
  touch $RPM_BUILD_ROOT/rootfile
  root=..
  while [ ! -e $RPM_BUILD_ROOT/%{_libdir}/${root}/rootfile ] ; do
	root=${root}/..
  done
  rm $RPM_BUILD_ROOT/rootfile

  ln -sf ${root}/%{_lib}/libdb-%{__soversion}.so $RPM_BUILD_ROOT/%{_libdir}/libdb.so
  ln -sf ${root}/%{_lib}/libdb-%{__soversion}.so $RPM_BUILD_ROOT/%{_libdir}/
  ln -sf libdb_cxx-%{__soversion}.so $RPM_BUILD_ROOT/%{_libdir}/libdb_cxx.so
fi

# Move the header files to a subdirectory, in case we're deploying on a
# system with multiple versions of DB installed.
mkdir -p ${RPM_BUILD_ROOT}%{_includedir}/db4
mv ${RPM_BUILD_ROOT}%{_includedir}/*.h ${RPM_BUILD_ROOT}%{_includedir}/db4/

# Create symlinks to includes so that "use <db.h> and link with -ldb" works.
for i in db.h db_cxx.h db_185.h; do
	ln -s db4/$i ${RPM_BUILD_ROOT}%{_includedir}
done

%ifarch %{java_arches}
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

%clean
rm -rf ${RPM_BUILD_ROOT}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post -p /sbin/ldconfig tcl

%postun -p /sbin/ldconfig tcl

%post -p /sbin/ldconfig java

%postun -p /sbin/ldconfig java

%files
%defattr(-,root,root)
%doc LICENSE README
/%{_lib}/libdb-%{__soversion}.so
%{_libdir}/libdb-%{__soversion}.so

%files cxx
%defattr(-,root,root)
%{_libdir}/libdb_cxx-%{__soversion}.so

%files utils
%defattr(-,root,root)
%{_bindir}/db*_archive
%{_bindir}/db*_checkpoint
%{_bindir}/db*_deadlock
%{_bindir}/db*_dump*
%{_bindir}/db*_hotbackup
%{_bindir}/db*_load
%{_bindir}/db*_printlog
%{_bindir}/db*_recover
%{_bindir}/db*_sql
%{_bindir}/db*_stat
%{_bindir}/db*_upgrade
%{_bindir}/db*_verify

%files devel
%defattr(-,root,root)
%doc	docs/*
%doc	examples_c examples_cxx
%{_libdir}/libdb.so
%{_libdir}/libdb_cxx.so
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/db.h
%{_includedir}/%{name}/db_185.h
%{_includedir}/%{name}/db_cxx.h
%{_includedir}/db.h
%{_includedir}/db_185.h
%{_includedir}/db_cxx.h

%files devel-static
%defattr(-,root,root)
%{_libdir}/libdb-%{__soversion}.a
%{_libdir}/libdb_cxx-%{__soversion}.a
%{_libdir}/libdb_tcl-%{__soversion}.a
%ifarch %{java_arches}
%{_libdir}/libdb_java-%{__soversion}.a
%endif

%files tcl
%defattr(-,root,root)
%{_libdir}/libdb_tcl-%{__soversion}.so

%ifarch %{java_arches}
%files java
%defattr(-,root,root)
%doc docs/java
%doc examples_java
%{_libdir}/libdb_java*.so
%{_datadir}/java/*.jar
%endif

%changelog
* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 4.8.30-4
- 为 Magic 3.0 重建

* Tue Feb 24 2009 Liu Di <liudidi@gmail.com> - 4.7.25-2
- 修正编译问题

* Fri Jul 25 2008 Liu Di <liudidi@gmail.com> - 4.7.25-1mgc
- 升级到 4.7.25
