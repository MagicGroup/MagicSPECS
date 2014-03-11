%define db45_version 4.5.20
%define db46_version 4.6.21
%define db47_version 4.7.25
%define db4_versions %{db45_version} %{db46_version} %{db47_version}
%define main_version %{db47_version}

%define _libdb_a	libdb-${soversion}.a
%define _libcxx_a	libdb_cxx-${soversion}.a

Summary: The Berkeley DB database compatibility library
Summary(zh_CN.UTF-8): 为兼容老版本的 Magic 提供的 Berkeley DB 库
Name: compat-db
Version: %{main_version}
Release: 4%{?dist}
Source0: http://download.oracle.com/berkeley-db/db-%{db45_version}.tar.gz
Source1: http://download.oracle.com/berkeley-db/db-%{db46_version}.tar.gz
Source2: http://download.oracle.com/berkeley-db/db-%{db47_version}.tar.gz
# license text extracted from tarball
Source3: LICENSE

Patch3: db-4.5.20-sparc64.patch
Patch4: db-4.5.20-glibc.patch
Patch5: db-4.6.21-1.85-compat.patch

# Upstream db-4.5.20 patches
Patch30: http://www.oracle.com/technology/products/berkeley-db/db/update/%{db45_version}/patch.%{db45_version}.1
Patch31: http://www.oracle.com/technology/products/berkeley-db/db/update/%{db45_version}/patch.%{db45_version}.2

# Upstream db-4.6.21 patches
Patch40: http://www.oracle.com/technology/products/berkeley-db/db/update/%{db46_version}/patch.%{db46_version}.1
Patch41: http://www.oracle.com/technology/products/berkeley-db/db/update/%{db46_version}/patch.%{db46_version}.2

# Upstream db-4.7.25 patches
Patch50: http://www.oracle.com/technology/products/berkeley-db/db/update/%{db47_version}/patch.4.7.25.1
Patch51: http://www.oracle.com/technology/products/berkeley-db/db/update/%{db47_version}/patch.4.7.25.2
Patch52: http://www.oracle.com/technology/products/berkeley-db/db/update/%{db47_version}/patch.4.7.25.3
Patch53: http://www.oracle.com/technology/products/berkeley-db/db/update/%{db47_version}/patch.4.7.25.4


URL: http://www.oracle.com/database/berkeley-db/
License: BSD
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
BuildRequires: findutils, libtool, perl, sed, ed
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: compat-db45%{?_isa} = %{db45_version}-%{release}
Requires: compat-db46%{?_isa} = %{db46_version}-%{release}
Requires: compat-db47%{?_isa} = %{db47_version}-%{release}

%description
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
This package contains various versions of Berkeley DB which were included in
previous releases of Red Hat Linux.

%description -l zh_CN.UTF-8
Berkeley 数据库 (Berkeley DB) 是一个编程工具包。它为传统的和客户机/服务
器程序提供嵌入的数据库支持。Berkeley DB 包括 B+tree、扩展的线形散列、固
定的和长短不同的记录存取方法、事务、上锁、记录日志、共享的内存缓存、以
及数据库恢复。Berkeley DB 支持 C、C++、Java、和 Perl API。它被许多程序
使用，包括 Python 和 Perl，因此它应该在所有系统上安装。

这个包提供了包含在之前的 Magic Linux 中的多个版本的 Berkeley DB。

%package -n compat-db-headers
Summary: The Berkeley DB database compatibility headers
Summary(zh_CN.UTF-8): Berkeley DB 数据库兼容头文件
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
BuildArch: noarch
Obsoletes: db4 < 4.5, db4-devel < 4.5, db4-utils < 4.5, db4-tcl < 4.5, db4-java < 4.5
Obsoletes: compat-db < 4.7.25-17

%description -n compat-db-headers
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
This package contains Berkeley DB library headers used for compatibility.

%description -n compat-db-headers -l zh_CN.UTF-8
Berkeley 数据库 (Berkeley DB) 是一个编程工具包。它为传统的和客户机/服务
器程序提供嵌入的数据库支持。Berkeley DB 包括 B+tree、扩展的线形散列、固
定的和长短不同的记录存取方法、事务、上锁、记录日志、共享的内存缓存、以
及数据库恢复。Berkeley DB 支持 C、C++、Java、和 Perl API。它被许多程序
使用，包括 Python 和 Perl，因此它应该在所有系统上安装。

这个包提供了 Berkeley 数据库兼容库头文件。

%package -n compat-db45
Summary: The Berkeley DB database %{db45_version} compatibility library
Summary(zh_CN.UTF-8): Berkeley DB 数据库 %{db45_version} 兼容库
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Requires: compat-db-headers = %{main_version}-%{release}
Version: %{db45_version}
Obsoletes: db1, db1-devel
Obsoletes: db2, db2-devel, db2-utils
Obsoletes: db3, db3-devel, db3-utils
Obsoletes: db31, db32, db3x
Obsoletes: db4 < 4.5, db4-devel < 4.5, db4-utils < 4.5, db4-tcl < 4.5, db4-java < 4.5
Obsoletes: compat-db < 4.6.21-5

%description -n compat-db45
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
This package contains Berkeley DB library version %{db45_version} used for compatibility.

%description -n compat-db45 -l zh_CN.UTF-8
Berkeley 数据库 (Berkeley DB) 是一个编程工具包。它为传统的和客户机/服务
器程序提供嵌入的数据库支持。Berkeley DB 包括 B+tree、扩展的线形散列、固
定的和长短不同的记录存取方法、事务、上锁、记录日志、共享的内存缓存、以
及数据库恢复。Berkeley DB 支持 C、C++、Java、和 Perl API。它被许多程序
使用，包括 Python 和 Perl，因此它应该在所有系统上安装。

这个包提供了包含在之前的 Magic Linux 中的多个版本的 Berkeley DB %{db45_version}。

%package -n compat-db46
Summary: The Berkeley DB database %{db46_version} compatibility library
Summary(zh_CN.UTF-8): Berkeley DB 数据库 %{db46_version} 兼容库
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Requires: compat-db-headers = %{main_version}-%{release}
Version: %{db46_version}
Obsoletes: db1, db1-devel
Obsoletes: db2, db2-devel, db2-utils
Obsoletes: db3, db3-devel, db3-utils
Obsoletes: db31, db32, db3x
Obsoletes: db4 < 4.6, db4-devel < 4.6, db4-utils < 4.6, db4-tcl < 4.6, db4-java < 4.6
Obsoletes: compat-db < 4.6.21-5

%description -n compat-db46
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
This package contains Berkeley DB library version %{db46_version} used for compatibility.

%description -n compat-db46 -l zh_CN.UTF-8
Berkeley 数据库 (Berkeley DB) 是一个编程工具包。它为传统的和客户机/服务
器程序提供嵌入的数据库支持。Berkeley DB 包括 B+tree、扩展的线形散列、固
定的和长短不同的记录存取方法、事务、上锁、记录日志、共享的内存缓存、以
及数据库恢复。Berkeley DB 支持 C、C++、Java、和 Perl API。它被许多程序
使用，包括 Python 和 Perl，因此它应该在所有系统上安装。

这个包提供了包含在之前的 Magic Linux 中的多个版本的 Berkeley DB %{db46_version}。

%package -n compat-db47
Summary: The Berkeley DB database %{db47_version} compatibility library
Summary(zh_CN.UTF-8): Berkeley DB 数据库 %{db47_version} 兼容库
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Requires: compat-db-headers = %{main_version}-%{release}
Version: %{db47_version}
Obsoletes: db1, db1-devel
Obsoletes: db2, db2-devel, db2-utils
Obsoletes: db3, db3-devel, db3-utils
Obsoletes: db31, db32, db3x
Obsoletes: db4 < 4.7, db4-devel < 4.7, db4-utils < 4.7, db4-tcl < 4.7, db4-java < 4.7
Obsoletes: compat-db < 4.6.21-5

%description -n compat-db47
The Berkeley Database (Berkeley DB) is a programmatic toolkit that provides
embedded database support for both traditional and client/server applications.
This package contains Berkeley DB library version %{db47_version} used for compatibility.

%description -n compat-db47 -l zh_CN.UTF-8
Berkeley 数据库 (Berkeley DB) 是一个编程工具包。它为传统的和客户机/服务
器程序提供嵌入的数据库支持。Berkeley DB 包括 B+tree、扩展的线形散列、固
定的和长短不同的记录存取方法、事务、上锁、记录日志、共享的内存缓存、以
及数据库恢复。Berkeley DB 支持 C、C++、Java、和 Perl API。它被许多程序
使用，包括 Python 和 Perl，因此它应该在所有系统上安装。

这个包提供了包含在之前的 Magic Linux 中的多个版本的 Berkeley DB %{db47_version}。

%prep
%setup -q -c -a 1 -a 2

pushd db-%{db45_version}
%patch30 -p0
%patch31 -p0
%patch3 -p1 -b .sparc64
%patch5 -p1 -b .compat
popd

pushd db-%{db46_version}
%patch40 -p0
%patch41 -p0
%patch3 -p1 -b .sparc64
%patch5 -p1 -b .compat
popd

pushd db-%{db47_version}
%patch50 -p0 -b .sequence
%patch51 -p0 -b .deadlock
%patch52 -p0 -b .dd-segfaults
%patch53 -p1 -b .java-api
%patch3 -p1 -b .sparc64
%patch5 -p1 -b .compat
popd

%patch4 -p1 -b .glibc

mkdir docs
for version in %{db4_versions} ; do
	mkdir docs/db-${version}
	install -m644 db*${version}/{README,LICENSE} docs/db-${version}
done
cp %{SOURCE3} .

%build
export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
for version in %{db4_versions} ; do
	pushd db-${version}/dist
	./s_config
	mkdir build_unix
	cd build_unix
	ln -s ../configure
	%configure --prefix=%{_prefix} \
		--enable-compat185 \
		--enable-shared --disable-static \
		--enable-rpc \
		--enable-cxx
	soversion=`echo ${version} | cut -f1,2 -d.`
	make libdb=%{_libdb_a} libcxx=%{_libcxx_a} %{?_smp_mflags}
	popd
done

# remove dangling tags symlink from examples.
rm -f examples_cxx/tags
rm -f examples_c/tags

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}

for version in %{db4_versions} ; do
	pushd db-${version}/dist/build_unix
	%makeinstall libdb=%{_libdb_a} libcxx=%{_libcxx_a}
	# Move headers to special directory to avoid conflicts
	mkdir -p ${RPM_BUILD_ROOT}%{_includedir}/db${version}
	mv db.h db_185.h db_cxx.h ${RPM_BUILD_ROOT}%{_includedir}/db${version}
	# Rename the utilities.
	major=`echo ${version} | cut -c1,3`
	for bin in ${RPM_BUILD_ROOT}%{_bindir}/*db_* ; do
		t=`echo ${bin} | sed "s,db_,db${major}_,g"`
		mv ${bin} ${t}
	done
	popd
done

# Nuke non-versioned symlinks and headers
rm -f ${RPM_BUILD_ROOT}%{_libdir}/libdb-4.so \
${RPM_BUILD_ROOT}%{_libdir}/libdb.so \
${RPM_BUILD_ROOT}%{_libdir}/libdb_cxx-4.so \
${RPM_BUILD_ROOT}%{_libdir}/libdb_cxx.so \
${RPM_BUILD_ROOT}%{_includedir}/db.h \
${RPM_BUILD_ROOT}%{_includedir}/db_185.h \
${RPM_BUILD_ROOT}%{_includedir}/db_cxx.h


# Make sure all shared libraries have the execute bit set.
chmod 755 ${RPM_BUILD_ROOT}%{_libdir}/libdb*.so*

# XXX Avoid Permission denied. strip when building as non-root.
chmod u+w ${RPM_BUILD_ROOT}%{_bindir} ${RPM_BUILD_ROOT}%{_bindir}/*

# Make %{_libdir}/db<version>/libdb.so symlinks to ease detection for autofoo
for version in %{db4_versions} ; do
	mkdir -p ${RPM_BUILD_ROOT}/%{_libdir}/db${version}
	pushd ${RPM_BUILD_ROOT}/%{_libdir}/db${version}
	ln -s ../../../%{_lib}/libdb-`echo ${version} | cut -b 1-3`.so libdb.so
	ln -s ../../../%{_lib}/libdb_cxx-`echo ${version} | cut -b 1-3`.so libdb_cxx.so
	popd
done


# On Linux systems, move the shared libraries to lib directory.
%ifos linux
if [ "%{_libdir}" != "%{_lib}" ]; then
	mkdir -p ${RPM_BUILD_ROOT}/%{_lib}
	mv ${RPM_BUILD_ROOT}%{_libdir}/libdb*?.?.so* ${RPM_BUILD_ROOT}/%{_lib}/
fi
%endif

# Remove unpackaged files.
rm -fr ${RPM_BUILD_ROOT}%{_libdir}/*.la
rm -fr ${RPM_BUILD_ROOT}%{_prefix}/docs/

%clean
rm -rf ${RPM_BUILD_ROOT}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)

%files -n compat-db-headers
%defattr(-,root,root)
%doc LICENSE
%{_includedir}/db%{db45_version}
%{_includedir}/db%{db46_version}
%{_includedir}/db%{db47_version}

%files -n compat-db45
%defattr(-,root,root)
%doc docs/db-%{db45_version}
%{_bindir}/db45*
%{_bindir}/berkeley_db45_svc
%ifos linux
/%{_lib}/libdb-4.5.so
/%{_lib}/libdb_cxx-4.5.so
%else
%{_libdir}/libdb-4.5.so
%{_libdir}/libdb_cxx-4.5.so
%endif
%{_libdir}/db%{db45_version}

%files -n compat-db46
%defattr(-,root,root)
%doc docs/db-%{db46_version}
%{_bindir}/db46*
%{_bindir}/berkeley_db46_svc
%ifos linux
/%{_lib}/libdb-4.6.so
/%{_lib}/libdb_cxx-4.6.so
%else
%{_libdir}/libdb-4.6.so
%{_libdir}/libdb_cxx-4.6.so
%endif
%{_libdir}/db%{db46_version}

%files -n compat-db47
%defattr(-,root,root)
%doc docs/db-%{db47_version}
%{_bindir}/db47*
%{_bindir}/berkeley_db47_svc
%ifos linux
/%{_lib}/libdb-4.7.so
/%{_lib}/libdb_cxx-4.7.so
%else
%{_libdir}/libdb-4.7.so
%{_libdir}/libdb_cxx-4.7.so
%endif
%{_libdir}/db%{db47_version}

%changelog
* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 4.7.25-4
- 为 Magic 3.0 重建

* Fri Jul 25 2008 Liu Di <liudidi@gmail.com> - 4.6.21-1mgc
- 重建
