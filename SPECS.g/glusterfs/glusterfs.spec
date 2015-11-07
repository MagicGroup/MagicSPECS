%global _hardened_build 1

%global _for_fedora_koji_builds 1

# uncomment and add '%' to use the prereltag for pre-releases
%global prereltag beta3

# if you wish to compile an rpm without rdma support, compile like this...
# rpmbuild -ta @PACKAGE_NAME@-@PACKAGE_VERSION@.tar.gz --without rdma
%{?_without_rdma:%global _without_rdma --disable-ibverbs}

# No RDMA Support on s390(x)
%ifarch s390 s390x
%global _without_rdma --disable-ibverbs
%endif

# if you wish to compile an rpm without epoll...
# rpmbuild -ta @PACKAGE_NAME@-@PACKAGE_VERSION@.tar.gz --without epoll
%{?_without_epoll:%global _without_epoll --disable-epoll}

# if you wish to compile an rpm without fusermount...
# rpmbuild -ta @PACKAGE_NAME@-@PACKAGE_VERSION@.tar.gz --without fusermount
%{?_without_fusermount:%global _without_fusermount --disable-fusermount}

# if you wish to compile an rpm without geo-replication support, compile like this...
# rpmbuild -ta @PACKAGE_NAME@-@PACKAGE_VERSION@.tar.gz --without georeplication
%{?_without_georeplication:%global _without_georeplication --disable-geo-replication}

# if you wish to compile an rpm without the OCF resource agents...
# rpmbuild -ta @PACKAGE_NAME@-@PACKAGE_VERSION@.tar.gz --without ocf
%{?_without_ocf:%global _without_ocf --without-ocf}

# if you wish to build rpms without syslog logging, compile like this
# rpmbuild -ta @PACKAGE_NAME@-@PACKAGE_VERSION@tar.gz --without syslog
%{?_without_syslog:%global _without_syslog --disable-syslog}

# disable syslog forcefully as rhel <= 6 doesn't have rsyslog or rsyslog-mmcount
%if ( 0%{?rhel} && 0%{?rhel} <= 6 )
%global _without_syslog --disable-syslog
%endif

# there is no systemtap support! Perhaps some day there will be
%global _without_systemtap --enable-systemtap=no

# if you wish to compile an rpm without the BD map support...
# rpmbuild -ta @PACKAGE_NAME@-@PACKAGE_VERSION@.tar.gz --without bd
%{?_without_bd:%global _without_bd --disable-bd-xlator}

%if ( 0%{?rhel} && 0%{?rhel} < 6 )
%define _without_bd --disable-bd-xlator
%endif

# if you wish to compile an rpm without the qemu-block support...
# rpmbuild -ta @PACKAGE_NAME@-@PACKAGE_VERSION@.tar.gz --without qemu-block
%{?_without_qemu_block:%global _without_qemu_block --disable-qemu-block}

%if ( 0%{?rhel} && 0%{?rhel} < 6 )
# xlators/features/qemu-block fails to build on RHEL5, disable it
%define _without_qemu_block --disable-qemu-block
%endif

%if ( 0%{?fedora} && 0%{?fedora} > 16 ) || ( 0%{?rhel} && 0%{?rhel} > 6 )
%global           _with_systemd true
%endif

# From https://fedoraproject.org/wiki/Packaging:Python#Macros
%if ( 0%{?rhel} && 0%{?rhel} <= 5 )
%{!?python_sitelib: %global python_sitelib %(python -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(python -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

Summary:          Cluster File System
%if ( 0%{_for_fedora_koji_builds} )
Name:             glusterfs
Version:          3.5.0
Release:          0.7%{?prereltag:.%{prereltag}}%{?dist}
Vendor:           Fedora Project
%else
Name:             @PACKAGE_NAME@
Version:          @PACKAGE_VERSION@
Release:          3%{?dist}
Vendor:           glusterfs.org
%endif
License:          GPLv2 or LGPLv3+
Group:            System Environment/Base
URL:              http://www.gluster.org/docs/index.php/GlusterFS
%if ( 0%{_for_fedora_koji_builds} )
Source0:           http://bits.gluster.org/pub/gluster/glusterfs/src/glusterfs-%{version}%{?prereltag}.tar.gz
Source1:          glusterd.sysconfig
Source2:          glusterfsd.sysconfig
Source3:          glusterfs-fuse.logrotate
Source4:          glusterd.logrotate
Source5:          glusterfsd.logrotate
Source6:          rhel5-load-fuse-modules
Source11:         glusterfsd.service
Source13:         glusterfsd.init
%else
Source0:          @PACKAGE_NAME@-@PACKAGE_VERSION@.tar.gz
%endif

BuildRoot:        %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%if ( 0%{?rhel} && 0%{?rhel} <= 5 )
BuildRequires:    python-simplejson
%endif
%if ( 0%{?_with_systemd:1} )
%if ( 0%{_for_fedora_koji_builds} )
%global glusterfsd_service %{S:%{SOURCE11}}
%endif
BuildRequires:    systemd-units
Requires(post):   systemd-units
Requires(preun):  systemd-units
Requires(postun): systemd-units
%define _init_enable()  /bin/systemctl enable %1.service ;
%define _init_disable() /bin/systemctl disable %1.service ;
%define _init_restart() /bin/systemctl try-restart %1.service ;
%define _init_stop()    /bin/systemctl stop %1.service ;
%define _init_install() install -D -p -m 0644 %1 %{buildroot}%{_unitdir}/%2.service ;
# can't seem to make a generic macro that works
%define _init_glusterd   %{_unitdir}/glusterd.service
%define _init_glusterfsd %{_unitdir}/glusterfsd.service
%else
%if ( 0%{_for_fedora_koji_builds} )
%global glusterfsd_service %{S:%{SOURCE13}}
%endif
Requires(post):   /sbin/chkconfig
Requires(preun):  /sbin/service
Requires(preun):  /sbin/chkconfig
Requires(postun): /sbin/service
%define _init_enable()  /sbin/chkconfig --add %1 ;
%define _init_disable() /sbin/chkconfig --del %1 ;
%define _init_restart() /sbin/service %1 condrestart &>/dev/null ;
%define _init_stop()    /sbin/service %1 stop &>/dev/null ;
%define _init_install() install -D -p -m 0755 %1 %{buildroot}%{_sysconfdir}/init.d/%2 ;
# can't seem to make a generic macro that works
%define _init_glusterd   %{_sysconfdir}/init.d/glusterd
%define _init_glusterfsd %{_sysconfdir}/init.d/glusterfsd
%endif

Requires:         %{name}-libs = %{version}-%{release}
BuildRequires:    bison flex
BuildRequires:    gcc make automake libtool
BuildRequires:    ncurses-devel readline-devel
BuildRequires:    libxml2-devel openssl-devel
BuildRequires:    libaio-devel
BuildRequires:    python-devel
BuildRequires:    python-ctypes
%if ( 0%{!?_without_systemtap:1} )
BuildRequires:    systemtap-sdt-devel
%endif
%if ( 0%{!?_without_bd:1} )
BuildRequires:    lvm2-devel
%endif
%if ( 0%{!?_without_qemu_block:1} )
BuildRequires:    glib2-devel
%endif
%if ( 0%{!?_without_georeplication:1} )
BuildRequires:    libattr-devel
%endif

Obsoletes:        hekafs
Obsoletes:        %{name}-common < %{version}-%{release}
Obsoletes:        %{name}-core < %{version}-%{release}
Provides:         %{name}-common = %{version}-%{release}
Provides:         %{name}-core = %{version}-%{release}
Obsoletes:        %{name}-ufo

# We do not want to generate useless provides and requires for xlator .so files
# Filter all generated:
#
# TODO: RHEL5 does not have a convenient solution
%if ( 0%{?rhel} == 6 )
    # filter_setup exists in RHEL6 only
    %filter_provides_in %{_libdir}/glusterfs/%{version}/
    %global __filter_from_req %{?__filter_from_req} | grep -v -P '^(?!lib).*\.so.*$'
    %filter_setup
%else
    # modern rpm and current Fedora do not generate requires when the
    # provides are filtered
    %global __provides_exclude_from ^%{_libdir}/glusterfs/%{version}/.*$
%endif

%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

%if ( 0%{?rhel} && 0%{?rhel} < 6 )
   # _sharedstatedir is not provided by RHEL5
   %define _sharedstatedir /var/lib
%endif

%description
GlusterFS is a clustered file-system capable of scaling to several
petabytes. It aggregates various storage bricks over Infiniband RDMA
or TCP/IP interconnect into one large parallel network file
system. GlusterFS is one of the most sophisticated file systems in
terms of features and extensibility.  It borrows a powerful concept
called Translators from GNU Hurd kernel. Much of the code in GlusterFS
is in user space and easily manageable.

This package includes the glusterfs binary, the glusterfsd daemon and the
gluster command line, libglusterfs and glusterfs translator modules common to
both GlusterFS server and client framework.

%package libs
Summary:          GlusterFS common libraries
Group:            Applications/File
%if ( 0%{!?_without_syslog:1} )
%if ( 0%{?fedora} ) || ( 0%{?rhel} && 0%{?rhel} > 6 )
Requires:         rsyslog-mmjsonparse
%endif
%if ( 0%{?rhel} && 0%{?rhel} == 6 )
Requires:         rsyslog-mmcount
%endif
%endif

%description libs
GlusterFS is a clustered file-system capable of scaling to several
petabytes. It aggregates various storage bricks over Infiniband RDMA
or TCP/IP interconnect into one large parallel network file
system. GlusterFS is one of the most sophisticated file systems in
terms of features and extensibility.  It borrows a powerful concept
called Translators from GNU Hurd kernel. Much of the code in GlusterFS
is in user space and easily manageable.

This package provides the base GlusterFS libraries

%package cli
Summary:          GlusterFS CLI
Group:            Applications/File
Requires:         %{name}-libs = %{version}-%{release}

%description cli
GlusterFS is a clustered file-system capable of scaling to several
petabytes. It aggregates various storage bricks over Infiniband RDMA
or TCP/IP interconnect into one large parallel network file
system. GlusterFS is one of the most sophisticated file systems in
terms of features and extensibility.  It borrows a powerful concept
called Translators from GNU Hurd kernel. Much of the code in GlusterFS
is in user space and easily manageable.

This package provides the GlusterFS CLI application and its man page

%if ( 0%{!?_without_rdma:1} )
%package rdma
Summary:          GlusterFS rdma support for ib-verbs
Group:            Applications/File
BuildRequires:    libibverbs-devel
BuildRequires:    librdmacm-devel
Requires:         %{name} = %{version}-%{release}

%description rdma
GlusterFS is a clustered file-system capable of scaling to several
petabytes. It aggregates various storage bricks over Infiniband RDMA
or TCP/IP interconnect into one large parallel network file
system. GlusterFS is one of the most sophisticated file systems in
terms of features and extensibility.  It borrows a powerful concept
called Translators from GNU Hurd kernel. Much of the code in GlusterFS
is in user space and easily manageable.

This package provides support to ib-verbs library.
%endif

%if ( 0%{!?_without_georeplication:1} )
%package geo-replication
Summary:          GlusterFS Geo-replication
Group:            Applications/File
Requires:         %{name} = %{version}-%{release}
Requires:         %{name}-server = %{version}-%{release}
Requires:         python python-ctypes

%description geo-replication
GlusterFS is a clustered file-system capable of scaling to several
peta-bytes. It aggregates various storage bricks over Infiniband RDMA
or TCP/IP interconnect into one large parallel network file
system. GlusterFS is one of the most sophisticated file system in
terms of features and extensibility.  It borrows a powerful concept
called Translators from GNU Hurd kernel. Much of the code in GlusterFS
is in userspace and easily manageable.

This package provides support to geo-replication.
%endif

%package fuse
Summary:          Fuse client
Group:            Applications/File
BuildRequires:    fuse-devel

Requires:         %{name} = %{version}-%{release}

Obsoletes:        %{name}-client < %{version}-%{release}
Provides:         %{name}-client = %{version}-%{release}

%description fuse
GlusterFS is a clustered file-system capable of scaling to several
petabytes. It aggregates various storage bricks over Infiniband RDMA
or TCP/IP interconnect into one large parallel network file
system. GlusterFS is one of the most sophisticated file systems in
terms of features and extensibility.  It borrows a powerful concept
called Translators from GNU Hurd kernel. Much of the code in GlusterFS
is in user space and easily manageable.

This package provides support to FUSE based clients.

%package server
Summary:          Clustered file-system server
Group:            System Environment/Daemons
Requires:         %{name} = %{version}-%{release}
Requires:         %{name}-cli = %{version}-%{release}
Requires:         %{name}-libs = %{version}-%{release}
Requires:         %{name}-fuse = %{version}-%{release}
%if ( 0%{?fedora} ) || ( 0%{?rhel} && 0%{?rhel} >= 6 )
Requires:         rpcbind
%else
Requires:         portmap
%endif

%description server
GlusterFS is a clustered file-system capable of scaling to several
petabytes. It aggregates various storage bricks over Infiniband RDMA
or TCP/IP interconnect into one large parallel network file
system. GlusterFS is one of the most sophisticated file systems in
terms of features and extensibility.  It borrows a powerful concept
called Translators from GNU Hurd kernel. Much of the code in GlusterFS
is in user space and easily manageable.

This package provides the glusterfs server daemon.

%package api
Summary:          Clustered file-system api library
Group:            System Environment/Daemons
Requires:         %{name} = %{version}-%{release}
Requires:         %{name}-devel = %{version}-%{release}
# we provide the Python package/namespace 'gluster'
Provides:         python-gluster = %{version}-%{release}

%description api
GlusterFS is a clustered file-system capable of scaling to several
petabytes. It aggregates various storage bricks over Infiniband RDMA
or TCP/IP interconnect into one large parallel network file
system. GlusterFS is one of the most sophisticated file systems in
terms of features and extensibility.  It borrows a powerful concept
called Translators from GNU Hurd kernel. Much of the code in GlusterFS
is in user space and easily manageable.

This package provides the glusterfs libgfapi library

%if ( 0%{!?_without_ocf:1} )
%package resource-agents
Summary:          OCF Resource Agents for GlusterFS
License:          GPLv3+
%if ( ! ( 0%{?rhel} && 0%{?rhel} < 6 ) )
# EL5 does not support noarch sub-packages
BuildArch:        noarch
%endif
# this Group handling comes from the Fedora resource-agents package
%if ( 0%{?fedora} || 0%{?centos_version} || 0%{?rhel} )
Group:            System Environment/Base
%else
Group:            Productivity/Clustering/HA
%endif
# for glusterd
Requires:         glusterfs-server
# depending on the distribution, we need pacemaker or resource-agents
Requires:         %{_prefix}/lib/ocf/resource.d

%description resource-agents
GlusterFS is a clustered file-system capable of scaling to several
petabytes. It aggregates various storage bricks over Infiniband RDMA
or TCP/IP interconnect into one large parallel network file
system. GlusterFS is one of the most sophisticated file systems in
terms of features and extensibility.  It borrows a powerful concept
called Translators from GNU Hurd kernel. Much of the code in GlusterFS
is in user space and easily manageable.

This package provides the resource agents which plug glusterd into
Open Cluster Framework (OCF) compliant cluster resource managers,
like Pacemaker.
%endif

%package devel
Summary:          Development Libraries
Group:            Development/Libraries
Requires:         %{name} = %{version}-%{release}

%description devel
GlusterFS is a clustered file-system capable of scaling to several
petabytes. It aggregates various storage bricks over Infiniband RDMA
or TCP/IP interconnect into one large parallel network file
system. GlusterFS is one of the most sophisticated file systems in
terms of features and extensibility.  It borrows a powerful concept
called Translators from GNU Hurd kernel. Much of the code in GlusterFS
is in user space and easily manageable.

This package provides the development libraries and include files.

%package api-devel
Summary:          Development Libraries
Group:            Development/Libraries
Requires:         %{name} = %{version}-%{release}
Requires:         %{name}-devel = %{version}-%{release}

%description api-devel
GlusterFS is a clustered file-system capable of scaling to several
petabytes. It aggregates various storage bricks over Infiniband RDMA
or TCP/IP interconnect into one large parallel network file
system. GlusterFS is one of the most sophisticated file systems in
terms of features and extensibility.  It borrows a powerful concept
called Translators from GNU Hurd kernel. Much of the code in GlusterFS
is in user space and easily manageable.

This package provides the api include files.

%package regression-tests
Summary:          Development Tools
Group:            Development/Tools
Requires:         %{name} = %{version}-%{release}
Requires:         %{name}-fuse = %{version}-%{release}
Requires:         %{name}-server = %{version}-%{release}
Requires:         perl(App::Prove) perl(Test::Harness) gcc util-linux-ng lvm2
Requires:         python attr dbench git nfs-utils xfsprogs

%description regression-tests
The Gluster Test Framework, is a suite of scripts used for
regression testing of Gluster.

%prep
%setup -q -n %{name}-%{version}%{?prereltag}

%build
./autogen.sh
%configure \
        %{?_without_rdma} \
        %{?_without_epoll} \
        %{?_without_fusermount} \
        %{?_without_georeplication} \
        %{?_without_ocf} \
        %{?_without_syslog} \
        %{?_without_bd} \
        %{?_without_qemu_block} \
        %{?_without_systemtap}

# fix hardening and remove rpath in shlibs
%if ( 0%{?fedora} && 0%{?fedora} > 17 ) || ( 0%{?rhel} && 0%{?rhel} > 6 )
sed -i 's| \\\$compiler_flags |&\\\$LDFLAGS |' libtool
%endif
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|' libtool

make %{?_smp_mflags}

pushd api/examples
FLAGS="$RPM_OPT_FLAGS" python setup.py build
popd

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
# install the gfapi Python library in /usr/lib/python*/site-packages
pushd api/examples
python setup.py install --skip-build --verbose --root %{buildroot}
popd
# Install include directory
mkdir -p %{buildroot}%{_includedir}/glusterfs
install -p -m 0644 libglusterfs/src/*.h \
    %{buildroot}%{_includedir}/glusterfs/
install -p -m 0644 contrib/uuid/*.h \
    %{buildroot}%{_includedir}/glusterfs/
# Following needed by hekafs multi-tenant translator
mkdir -p %{buildroot}%{_includedir}/glusterfs/rpc
install -p -m 0644 rpc/rpc-lib/src/*.h \
    %{buildroot}%{_includedir}/glusterfs/rpc/
install -p -m 0644 rpc/xdr/src/*.h \
    %{buildroot}%{_includedir}/glusterfs/rpc/
mkdir -p %{buildroot}%{_includedir}/glusterfs/server
install -p -m 0644 xlators/protocol/server/src/*.h \
    %{buildroot}%{_includedir}/glusterfs/server/
%if ( 0%{_for_fedora_koji_builds} )
install -D -p -m 0644 %{SOURCE1} \
    %{buildroot}%{_sysconfdir}/sysconfig/glusterd
install -D -p -m 0644 %{SOURCE2} \
    %{buildroot}%{_sysconfdir}/sysconfig/glusterfsd
%else
install -D -p -m 0644 extras/glusterd-sysconfig \
    %{buildroot}%{_sysconfdir}/sysconfig/glusterd
%endif

%if ( 0%{_for_fedora_koji_builds} )
%if ( 0%{?rhel} && 0%{?rhel} <= 5 )
install -D -p -m 0755 %{SOURCE6} \
    %{buildroot}%{_sysconfdir}/sysconfig/modules/glusterfs-fuse.modules
%endif
%endif

mkdir -p %{buildroot}%{_localstatedir}/log/glusterd
mkdir -p %{buildroot}%{_localstatedir}/log/glusterfs
mkdir -p %{buildroot}%{_localstatedir}/log/glusterfsd
mkdir -p %{buildroot}%{_localstatedir}/run/gluster

# Remove unwanted files from all the shared libraries
find %{buildroot}%{_libdir} -name '*.a' -delete
find %{buildroot}%{_libdir} -name '*.la' -delete

# Remove installed docs, the ones we want are included by %%doc, in
# /usr/share/doc/glusterfs or /usr/share/doc/glusterfs-x.y.z depending
# on the distribution
%if ( 0%{?fedora} && 0%{?fedora} > 19 ) || ( 0%{?rhel} && 0%{?rhel} > 6 )
rm -rf %{buildroot}%{_pkgdocdir}/*
%else
rm -rf %{buildroot}%{_defaultdocdir}/%{name}
mkdir -p %{buildroot}%{_pkgdocdir}
%endif
head -50 ChangeLog > ChangeLog.head && mv ChangeLog.head ChangeLog
cat << EOM >> ChangeLog

More commit messages for this ChangeLog can be found at
https://forge.gluster.org/glusterfs-core/glusterfs/commits/v%{version}%{?prereltag}
EOM

# Remove benchmarking and other unpackaged files
%if ( 0%{?rhel} && 0%{?rhel} < 6 )
rm -rf %{buildroot}/benchmarking
rm -f %{buildroot}/glusterfs-mode.el
rm -f %{buildroot}/glusterfs.vim
%else
# make install always puts these in %%{_defaultdocdir}/%%{name} so don't
# use %%{_pkgdocdir}; that will be wrong on later Fedora distributions
rm -rf %{buildroot}%{_defaultdocdir}/%{name}/benchmarking
rm -f %{buildroot}%{_defaultdocdir}/%{name}/glusterfs-mode.el
rm -f %{buildroot}%{_defaultdocdir}/%{name}/glusterfs.vim
%endif

# Create working directory
mkdir -p %{buildroot}%{_sharedstatedir}/glusterd

# Update configuration file to /var/lib working directory
sed -i 's|option working-directory /etc/glusterd|option working-directory %{_sharedstatedir}/glusterd|g' \
    %{buildroot}%{_sysconfdir}/glusterfs/glusterd.vol

# Install glusterfsd .service or init.d file
%if ( 0%{_for_fedora_koji_builds} )
%_init_install %{glusterfsd_service} glusterfsd
%endif

%if ( 0%{_for_fedora_koji_builds} )
# Client logrotate entry
install -D -p -m 0644 %{SOURCE3} \
    %{buildroot}%{_sysconfdir}/logrotate.d/glusterfs-fuse

# Server logrotate entry
install -D -p -m 0644 %{SOURCE4} \
    %{buildroot}%{_sysconfdir}/logrotate.d/glusterd
# Legacy server logrotate entry
install -D -p -m 0644 %{SOURCE5} \
    %{buildroot}%{_sysconfdir}/logrotate.d/glusterfsd
%else
install -D -p -m 0644 extras/glusterfs-logrotate \
    %{buildroot}%{_sysconfdir}/logrotate.d/glusterfs
%endif

%if ( 0%{!?_without_georeplication:1} )
# geo-rep ghosts
mkdir -p %{buildroot}%{_sharedstatedir}/glusterd/geo-replication
touch %{buildroot}%{_sharedstatedir}/glusterd/geo-replication/gsyncd_template.conf
install -D -p -m 0644 extras/glusterfs-georep-logrotate \
    %{buildroot}%{_sysconfdir}/logrotate.d/glusterfs-georep
%endif

%if ( 0%{!?_without_syslog:1} )
%if ( 0%{?fedora} ) || ( 0%{?rhel} && 0%{?rhel} > 6 )
install -D -p -m 0644 extras/gluster-rsyslog-7.2.conf \
    %{buildroot}%{_sysconfdir}/rsyslog.d/gluster.conf.example
%endif

%if ( 0%{?rhel} && 0%{?rhel} == 6 )
install -D -p -m 0644 extras/gluster-rsyslog-5.8.conf \
    %{buildroot}%{_sysconfdir}/rsyslog.d/gluster.conf.example
%endif

%if ( 0%{?fedora} ) || ( 0%{?rhel} && 0%{?rhel} >= 6 )
install -D -p -m 0644 extras/logger.conf.example \
    %{buildroot}%{_sysconfdir}/glusterfs/logger.conf.example
%endif
%endif

# the rest of the ghosts
touch %{buildroot}%{_sharedstatedir}/glusterd/glusterd.info
touch %{buildroot}%{_sharedstatedir}/glusterd/options
mkdir -p %{buildroot}%{_sharedstatedir}/glusterd/hooks
mkdir -p %{buildroot}%{_sharedstatedir}/glusterd/hooks/1
mkdir -p %{buildroot}%{_sharedstatedir}/glusterd/hooks/1/stop
mkdir -p %{buildroot}%{_sharedstatedir}/glusterd/hooks/1/stop/post
mkdir -p %{buildroot}%{_sharedstatedir}/glusterd/hooks/1/stop/pre
mkdir -p %{buildroot}%{_sharedstatedir}/glusterd/hooks/1/start
mkdir -p %{buildroot}%{_sharedstatedir}/glusterd/hooks/1/start/post
mkdir -p %{buildroot}%{_sharedstatedir}/glusterd/hooks/1/start/pre
mkdir -p %{buildroot}%{_sharedstatedir}/glusterd/hooks/1/remove-brick
mkdir -p %{buildroot}%{_sharedstatedir}/glusterd/hooks/1/remove-brick/post
mkdir -p %{buildroot}%{_sharedstatedir}/glusterd/hooks/1/remove-brick/pre
mkdir -p %{buildroot}%{_sharedstatedir}/glusterd/hooks/1/add-brick
mkdir -p %{buildroot}%{_sharedstatedir}/glusterd/hooks/1/add-brick/post
mkdir -p %{buildroot}%{_sharedstatedir}/glusterd/hooks/1/add-brick/pre
mkdir -p %{buildroot}%{_sharedstatedir}/glusterd/hooks/1/set
mkdir -p %{buildroot}%{_sharedstatedir}/glusterd/hooks/1/set/post
mkdir -p %{buildroot}%{_sharedstatedir}/glusterd/hooks/1/set/pre
mkdir -p %{buildroot}%{_sharedstatedir}/glusterd/hooks/1/create
mkdir -p %{buildroot}%{_sharedstatedir}/glusterd/hooks/1/create/post
mkdir -p %{buildroot}%{_sharedstatedir}/glusterd/hooks/1/create/pre
mkdir -p %{buildroot}%{_sharedstatedir}/glusterd/hooks/1/delete
mkdir -p %{buildroot}%{_sharedstatedir}/glusterd/hooks/1/delete/post
mkdir -p %{buildroot}%{_sharedstatedir}/glusterd/hooks/1/delete/pre
mkdir -p %{buildroot}%{_sharedstatedir}/glusterd/hooks/1/copy-file
mkdir -p %{buildroot}%{_sharedstatedir}/glusterd/hooks/1/copy-file/post
mkdir -p %{buildroot}%{_sharedstatedir}/glusterd/hooks/1/copy-file/pre
mkdir -p %{buildroot}%{_sharedstatedir}/glusterd/hooks/1/gsync-create
mkdir -p %{buildroot}%{_sharedstatedir}/glusterd/hooks/1/gsync-create/post
mkdir -p %{buildroot}%{_sharedstatedir}/glusterd/hooks/1/gsync-create/pre
mkdir -p %{buildroot}%{_sharedstatedir}/glusterd/glustershd
mkdir -p %{buildroot}%{_sharedstatedir}/glusterd/peers
mkdir -p %{buildroot}%{_sharedstatedir}/glusterd/vols
mkdir -p %{buildroot}%{_sharedstatedir}/glusterd/groups
mkdir -p %{buildroot}%{_sharedstatedir}/glusterd/nfs/run
touch %{buildroot}%{_sharedstatedir}/glusterd/nfs/nfs-server.vol
touch %{buildroot}%{_sharedstatedir}/glusterd/nfs/run/nfs.pid

install -p -m 0744 extras/hook-scripts/S56glusterd-geo-rep-create-post.sh \
    %{buildroot}%{_sharedstatedir}/glusterd/hooks/1/gsync-create/post

find ./tests ./run-tests.sh -type f | cpio -pd %{buildroot}%{_prefix}/share/glusterfs

%clean
rm -rf %{buildroot}

%post
%if ( 0%{!?_without_syslog:1} )
%if ( 0%{?fedora} ) || ( 0%{?rhel} && 0%{?rhel} >= 6 )
%_init_restart rsyslog
%endif
%endif

%postun
%if ( 0%{!?_without_syslog:1} )
%if ( 0%{?fedora} ) || ( 0%{?rhel} && 0%{?rhel} >= 6 )
%_init_restart rsyslog
%endif
%endif

%files
%doc ChangeLog COPYING-GPLV2 COPYING-LGPLV3 README THANKS
%config(noreplace) %{_sysconfdir}/logrotate.d/*
%config(noreplace) %{_sysconfdir}/sysconfig/*
%if ( 0%{!?_without_syslog:1} )
%if ( 0%{?fedora} ) || ( 0%{?rhel} && 0%{?rhel} >= 6 )
%{_sysconfdir}/rsyslog.d/gluster.conf.example
%endif
%endif
%{_libdir}/glusterfs
%{_sbindir}/glusterfs*
%{_mandir}/man8/*gluster*.8*
%exclude %{_mandir}/man8/gluster.8*
%dir %{_localstatedir}/log/glusterfs
%dir %{_localstatedir}/run/gluster
%dir %{_sharedstatedir}/glusterd
%if ( 0%{!?_without_rdma:1} )
%exclude %{_libdir}/glusterfs/%{version}%{?prereltag}/rpc-transport/rdma*
%endif
# server-side, etc., xlators in other RPMs
%exclude %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/mount/api*
%exclude %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/mount/fuse*
%exclude %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/storage*
%exclude %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features/posix*
%exclude %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/protocol/server*
%exclude %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/mgmt*
%exclude %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/nfs*
# sample xlators not generally used or usable
%exclude %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/encryption/rot-13*
%exclude %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features/mac-compat*
%exclude %{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/testing/performance/symlink-cache*

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files libs
%{_libdir}/*.so.*
%exclude %{_libdir}/libgfapi.*

%files cli
%{_sbindir}/gluster
%{_mandir}/man8/gluster.8*

%if ( 0%{!?_without_rdma:1} )
%files rdma
%{_libdir}/glusterfs/%{version}%{?prereltag}/rpc-transport/rdma*
%endif

%if ( 0%{!?_without_georeplication:1} )
%post geo-replication
#restart glusterd.
if [ $1 -ge 1 ]; then
    %_init_restart glusterd
fi

%files geo-replication
%{_sysconfdir}/logrotate.d/glusterfs-georep
%{_libexecdir}/glusterfs/gsyncd
%{_libexecdir}/glusterfs/python/syncdaemon/*
%{_libexecdir}/glusterfs/gverify.sh
%{_libexecdir}/glusterfs/peer_add_secret_pub
%{_libexecdir}/glusterfs/peer_gsec_create
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/geo-replication
%dir %{_sharedstatedir}/glusterd/hooks
%dir %{_sharedstatedir}/glusterd/hooks/1
%dir %{_sharedstatedir}/glusterd/hooks/1/gsync-create
%dir %{_sharedstatedir}/glusterd/hooks/1/gsync-create/post
%{_sharedstatedir}/glusterd/hooks/1/gsync-create/post/S56glusterd-geo-rep-create-post.sh
%{_datadir}/glusterfs/scripts/get-gfid.sh
%{_datadir}/glusterfs/scripts/slave-upgrade.sh
%{_datadir}/glusterfs/scripts/gsync-upgrade.sh
%{_datadir}/glusterfs/scripts/generate-gfid-file.sh
%{_datadir}/glusterfs/scripts/gsync-sync-gfid
%ghost %attr(0644,-,-) %{_sharedstatedir}/glusterd/geo-replication/gsyncd_template.conf
%endif

%files fuse
%if ( 0%{_for_fedora_koji_builds} )
%config(noreplace) %{_sysconfdir}/logrotate.d/glusterfs-fuse
%endif
%{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/mount/fuse*
/sbin/mount.glusterfs
%if ( 0%{!?_without_fusermount:1} )
%{_bindir}/fusermount-glusterfs
%endif
%if ( 0%{_for_fedora_koji_builds} )
%if ( 0%{?rhel} && 0%{?rhel} <= 5 )
%{_sysconfdir}/sysconfig/modules/glusterfs-fuse.modules
%endif
%endif

%files server
%doc extras/clear_xattrs.sh
%if ( 0%{_for_fedora_koji_builds} )
%config(noreplace) %{_sysconfdir}/logrotate.d/glusterd
%endif
%config(noreplace) %{_sysconfdir}/sysconfig/glusterd
%config(noreplace) %{_sysconfdir}/glusterfs
# %%dir %{_sharedstatedir}/glusterd/groups
# %%config(noreplace) %{_sharedstatedir}/glusterd/groups/virt
# Legacy configs
%if ( 0%{_for_fedora_koji_builds} )
%config(noreplace) %{_sysconfdir}/logrotate.d/glusterfsd
%config(noreplace) %{_sysconfdir}/sysconfig/glusterfsd
%endif
# init files
%_init_glusterd
%if ( 0%{_for_fedora_koji_builds} )
%_init_glusterfsd
%endif
# binaries
%{_sbindir}/glusterd
%{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/storage*
%{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/features/posix*
%{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/protocol/server*
%{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/mgmt*
%{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/nfs*
# hack to work around old rpm/rpmbuild %%doc misfeature
%ghost %attr(0644,-,-) %config(noreplace) %{_sharedstatedir}/glusterd/glusterd.info
%ghost %attr(0600,-,-) %{_sharedstatedir}/glusterd/options
# This is really ugly, but I have no idea how to mark these directories in
# any other way. They should belong to the glusterfs-server package, but 
# don't exist after installation. They are generated on the first start...
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/stop
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/stop/post
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/stop/pre
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/start
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/start/post
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/start/pre
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/remove-brick
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/remove-brick/post
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/remove-brick/pre
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/add-brick
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/add-brick/post
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/add-brick/pre
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/set
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/set/post
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/set/pre
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/create
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/create/post
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/create/pre
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/delete
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/delete/post
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/hooks/1/delete/pre
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/glustershd
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/vols
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/peers
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/groups
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/nfs
%ghost      %attr(0600,-,-) %{_sharedstatedir}/glusterd/nfs/nfs-server.vol
%ghost %dir %attr(0755,-,-) %{_sharedstatedir}/glusterd/nfs/run
%ghost      %attr(0600,-,-) %{_sharedstatedir}/glusterd/nfs/run/nfs.pid

%post api -p /sbin/ldconfig

%postun api -p /sbin/ldconfig

%files api
%exclude %{_libdir}/*.so
%{_libdir}/libgfapi.*
%{_libdir}/glusterfs/%{version}%{?prereltag}/xlator/mount/api*
%{python_sitelib}/*

%if ( 0%{!?_without_ocf:1} )
%files resource-agents
# /usr/lib is the standard for OCF, also on x86_64
%{_prefix}/lib/ocf/resource.d/glusterfs
%endif

%files devel
%{_includedir}/glusterfs
%exclude %{_includedir}/glusterfs/y.tab.h
%exclude %{_includedir}/glusterfs/api
%exclude %{_libdir}/libgfapi.so
%{_libdir}/*.so

%files api-devel
%{_libdir}/pkgconfig/glusterfs-api.pc
%{_libdir}/pkgconfig/libgfchangelog.pc
%{_libdir}/libgfapi.so
%{_includedir}/glusterfs/api/*

%files regression-tests
%defattr(-,root,root,-)
%{_prefix}/share/glusterfs/*
%exclude %{_prefix}/share/glusterfs/tests/basic/rpm.t

%post server
# Legacy server
%_init_enable glusterd
%_init_enable glusterfsd

# hack to work around old rpm/rpmbuild %%doc misfeature
%if ( 0%{?rhel} && 0%{?rhel} < 7 )
if [ -d %{_pkgdocdir}.tmp ]; then
    cp -p %{_pkgdocdir}.tmp/* %{_pkgdocdir}/
    rm -rf %{_pkgdocdir}.tmp/*
%endif

# Genuine Fedora (and EPEL) builds never put gluster files in /etc; if
# there are any files in /etc from a prior gluster.org install, move them
# to /var/lib. (N.B. Starting with 3.3.0 all gluster files are in /var/lib
# in gluster.org RPMs.) Be careful to copy them on the off chance that
# /etc and /var/lib are on separate file systems
if [ -d /etc/glusterd -a ! -h %{_sharedstatedir}/glusterd ]; then
    mkdir -p %{_sharedstatedir}/glusterd
    cp -a /etc/glusterd %{_sharedstatedir}/glusterd
    rm -rf /etc/glusterd
    ln -sf %{_sharedstatedir}/glusterd /etc/glusterd
fi

# Rename old volfiles in an RPM-standard way.  These aren't actually
# considered package config files, so %%config doesn't work for them.
if [ -d %{_sharedstatedir}/glusterd/vols ]; then
    for file in $(find %{_sharedstatedir}/glusterd/vols -name '*.vol'); do
        newfile=${file}.rpmsave
        echo "warning: ${file} saved as ${newfile}"
        cp ${file} ${newfile}
    done
fi

# add marker translator
# but first make certain that there are no old libs around to bite us
# BZ 834847
if [ -e /etc/ld.so.conf.d/glusterfs.conf ]; then
    rm -f /etc/ld.so.conf.d/glusterfs.conf
    /sbin/ldconfig
fi
pidof -c -o %PPID -x glusterd &> /dev/null
if [ $? -eq 0 ]; then
    kill -9 `pgrep -f gsyncd.py` &> /dev/null

    killall glusterd &> /dev/null
    glusterd --xlator-option *.upgrade=on -N
else
    glusterd --xlator-option *.upgrade=on -N
fi

%preun server
if [ $1 -eq 0 ]; then
    if [ -f %_init_glusterfsd ]; then
        %_init_stop glusterfsd
    fi
    %_init_stop glusterd
    if [ -f %_init_glusterfsd ]; then
        %_init_disable glusterfsd
    fi
    %_init_disable glusterd
fi
if [ $1 -ge 1 ]; then
    if [ -f %_init_glusterfsd ]; then
        %_init_restart glusterfsd
    fi
    %_init_restart glusterd
fi

%changelog
* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 3.5.0-0.7.beta3
- 为 Magic 3.0 重建

* Sat Sep 19 2015 Liu Di <liudidi@gmail.com> - 3.5.0-0.6.beta3
- 为 Magic 3.0 重建

* Tue Feb 11 2014 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.5.0-0.5.beta3
- GlusterFS 3.5.0 beta3 , glusterfs-3.5.0-0.5beta3

* Mon Jan 27 2014 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.5.0-0.4.beta2
- GlusterFS 3.5.0 beta2 , glusterfs-3.5.0-0.4beta2

* Thu Jan 16 2014 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.5.0-0.3.beta1
- GlusterFS 3.5.0 beta1 , glusterfs-3.5.0-0.1beta1

* Thu Jan 16 2014 Ville Skyttä <ville.skytta@iki.fi> - 3.5.0-0.2.beta1
- Drop unnecessary ldconfig calls, do remaining ones without shell.
- Drop INSTALL from docs.

* Wed Jan 15 2014 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.5.0-0.1.beta1
- GlusterFS 3.5.0 beta1 , glusterfs-3.5.0-0.1beta1

* Fri Dec 6 2013 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.5.0-0.1.qa3
- GlusterFS 3.5.0 QA3 , glusterfs-3.5.0-0.1qa3

* Wed Nov 6 2013 Kaleb S. KEITHLEY <kkeithle[at]redhat.com>
- obsolete glusterfs-ufo (#1025059)
- ownership of /usr/share/doc/glusterfs(-x.y.z) (#846737)
- clear_xattrs.sh belongs in /usr/share/doc/glusterfs(-x.y.z), not
  in /usr/share/doc/glusterfs-server(-x.y.z)
- remove defattr (per pkg review of another package)
- don't use %%{__foo} macros (per package review of another package)

* Sun Oct 27 2013 Niels de Vos <ndevos@redhat.com> - 3.4.1-3
- Correctly start+stop glusterfsd.service (#1022542)
- fix "warning: File listed twice: .../glusterd.info" while building

* Sat Oct 26 2013 Niels de Vos <ndevos@redhat.com>
- add base-port config option to /etc/glusterd/glusterd.vol (#1023653)

* Wed Oct 9 2013 Kaleb S. KEITHLEY <kkeithle[at]redhat.com>
- nit, sync with upstream spec

* Wed Oct 9 2013 Niels de Vos <ndevos@redhat.com>
- glusterfs-api-devel requires glusterfs-devel (#1016938, #1017094)

* Tue Oct 1 2013 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.4.1-2
- resurrect /etc/init.d/glusterfsd, BUG 1014242

* Fri Sep 27 2013 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.4.1-1
- GlusterFS 3.4.1 GA, glusterfs-3.4.1-1

* Thu Sep 26 2013 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.4.1-0.2rc1
- scratch build for community

* Wed Sep 11 2013 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.4.1-0.1qa1
- scratch build for community

* Fri Sep 6 2013 Niels de Vos <devos@fedoraproject.org>
- fix "warning: File listed twice: .../glusterd.info" while building

* Tue Aug 6 2013 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.4.0-8
- glusterfs-server requires glusterfs-cli

* Mon Aug 5 2013 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.4.0-7
- glusterfs requires glusterfs-libs

* Mon Aug 5 2013 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.4.0-6
- glusterfs-cli RPM to simplify dependencies for vdsm

* Mon Aug 5 2013 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.4.0-5
- there is no systemtap/dtrace support; don't even pretend

* Fri Aug 2 2013 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.4.0-4
- sync changes from upstream glusterfs.spec.in, including addition of
  glusterfs-libs RPM to simplify dependencies for qemu-kvm

* Thu Jul 25 2013 Kaleb S. KEITHLEY <kkeithle[at]redhat.com>
- remove gsyncd from glusterfs, it's redundant with glusterfs-geo-rep
  ready for next build

* Thu Jul 25 2013 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.4.0-3
- sync changes from upstream glusterfs.spec.in, and esp. glusterd.service
  from gluster w/o Wants=glusterfsd.service

* Thu Jul 18 2013 Kaleb S. KEITHLEY <kkeithle[at]redhat.com>
- sync changes from upstream glusterfs.spec.in, ready for next build

* Tue Jul 16 2013 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.4.0-2
- tag /var/lib/glusterd/glusterd.info as %%config

* Tue Jul 16 2013 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.2.2-2
- tag /var/lib/glusterd/glusterd.info as %%config

* Fri Jul 12 2013 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.4.0-1
- GlusterFS 3.4.0 GA, glusterfs-3.4.0-1

* Mon Jul 8 2013 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.4.0-0.9.beta4
- add Obsolete: glusterfs-swift where we use openstack-swift
- prerelease 3.4.0beta4 for oVirt/vdsm dependencies in Fedora19

* Fri Jul 5 2013 Niels de Vos <devos@fedoraproject.org>
- include xlators/mount/api.so in the glusterfs-api package

* Wed Jul 3 2013 Niels de Vos <devos@fedoraproject.org>
- correct AutoRequires filtering on recent Fedora (#972465)

* Fri Jun 28 2013 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.4.0-0.8.beta4
- prerelease 3.4.0beta4 for oVirt/vdsm dependencies in Fedora19

* Thu Jun 27 2013 Niels de Vos <devos@fedoraproject.org>
- correct trimming the ChangeLog, keep the recent messages (#963027)
- remove the umount.glusterfs helper (#640620)

* Wed Jun 26 2013 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.4.0-0.7.beta3
- prerelease 3.4.0beta3 for oVirt/vdsm dependencies in Fedora19
- libgfapi and xlator/mount/api dependency fix

* Tue Jun 11 2013 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.4.0-0.6.beta3
- prerelease 3.4.0beta3 for oVirt/vdsm dependencies in Fedora19

* Wed May 29 2013 Niels de Vos <devos@fedoraproject.org>
- automatically load the fuse module on EL5
- there is no need to require the unused /usr/bin/fusermount
- fix building on EL5

* Mon May 27 2013 Niels de Vos <devos@fedoraproject.org>
- include glusterfs-api.pc in the -devel subpackage

* Fri May 24 2013 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.4.0-0.5.beta2
- prerelease 3.4.0beta2 for oVirt/vdsm dependencies in Fedora19

* Thu May 9 2013 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.4.0-0.4.beta1
- prerelease 3.4.0beta1 for oVirt/vdsm dependencies in Fedora19

* Wed May 8 2013 Niels de Vos <devos@fedoraproject.org>
- include all Sources and Patches into the src.rpm

* Tue May 7 2013 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.4.0-0.1.beta1
- prerelease 3.4.0beta1 for oVirt/vdsm dependencies in Fedora19

* Mon Apr 29 2013 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.3.1-14
- include backport of G4S/UFO multi-volume fix

* Fri Apr 19 2013 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.4.0-0.3alpha3
- #else -> %%else, a twisty maze of passages, all alike

* Thu Apr 18 2013 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.4.0-0.2alpha3
- prerelease 3.4.0alpha3 for oVirt/vdsm dependencies in Fedora19
- RHEL6 still needs the patches applied, even with grizzly
- resource-agents -> noarch

* Wed Apr 17 2013 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.4.0-0.1alpha3
- prerelease 3.4.0alpha3 for oVirt/vdsm dependencies in Fedora19

* Wed Apr 17 2013 Niels de Vos <devos@fedoraproject.org> - 3.3.1-13
- remove unused requires for xlator .so files and private libraries (RHBZ#95212

* Mon Apr 15 2013 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.3.1-12
- add glusterfs-3.3.1.rpc.rpcxprt.rdma.name.c.patch, BZ 920332
- add %%{prereltag} for upcoming 3.3.2 and 3.4.0 alpha and beta builds
- add librdmacm-devel for rdma builds

* Mon Apr 15 2013 Niels de Vos <devos@fedoraproject.org>
- Remove useless provides for xlator .so files and private libraries

* Wed Apr 10 2013 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.4.0-0.1alpha2
- prerelease 3.4.0alpha2 for oVirt/vdsm dependencies in Fedora19

* Wed Mar 6 2013 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.3.1-11
- /var/run/gluster - sync with gluster.org git
- Requires: portmap for rhel5 instead of rpcbind

* Tue Feb 5 2013 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.3.1-10
- sync with glusterfs.spec(.in) from gluster.org git source

* Wed Jan 30 2013 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.3.1-9
- essex/folsom typo, glusterfs-ufo %%files conflicts with glusterfs-swift-*

* Thu Jan 10 2013 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.3.1-8
- revised patch to DiskFile.py for stalled GET

* Wed Jan 9 2013 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.3.1-7
- additional file ownerships and associated %%ghosts from upstream
- add BuildRequires libaio-devel to auto-enable AIO in configure,
  overlooked since 3.3.1-1.

* Fri Dec 21 2012 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.3.1-6
- fix object get, missing iter_hook param in DiskFile::__init__

* Mon Dec 17 2012 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.3.1-5
- Update to OpenStack Swift 1.7.4 (Folsom)

* Fri Dec 7 2012 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.3.1-4
- Swift+UFO, now with less swift forkage. Specifically the only patches
  to swift are those already used for the Fedora openstack-swift packages
  _plus_ our backport of the upstream constraints config changes that have
  been accepted into grizzly.

* Fri Nov 16 2012 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.3.1-3
- add Requires: rpcbind for minimum install systems where rpcbind isn't
  installed; usually this is a no-op.
- Better logic to preserve contents of /etc/glusterd

* Wed Oct 31 2012 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.3.1-2
- Synchronize with openstack-swift-1.4.8 packaging changes, including
  systemd .service files and align with the matching sets of patches

* Thu Oct 11 2012 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.3.1-1
- GlusterFS-3.3.1
- save swift .conf files correctly during upgrade
- fix glusterd restart in %%post geo-replication

* Wed Sep 19 2012 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.3.0-11
- condrestart glusterfsd then glusterd in %%preun server

* Wed Sep 19 2012 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.3.0-10
- fix additional python dependencies, esp. for rhel

* Tue Sep 18 2012 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.3.0-9
- python-paste-deploy on RHEL 6, glusterfsd.init

* Thu Sep 13 2012 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.3.0-8
- fix for glusterfs SEGV, BZ 856704, revised

* Wed Sep 12 2012 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.3.0-7
- fix for glusterfs SEGV, BZ 856704

* Fri Sep 7 2012 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.3.0-6
- glusterfs.spec cleanup

* Mon Aug 27 2012 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.2.7-2
- fix SEGV in glusterd-rpc-ops.c, BZ 837684, f17 only.

* Sun Aug 12 2012 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.3.0-5
- now with UFO (openstack-swift) except on el5

* Fri Aug 10 2012 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.3.0-4
- now with UFO (openstack-swift)

* Wed Jul 18 2012 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.3.0-3
- fix segv in cmd_heal_volume_brick_out (RHEL seems particularly
  sensitive to this bug.)

* Thu Jul 5 2012 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.3.0-2
- selected fixes to glusterfs.spec for BZs 826836, 826855, 829734, 834847

* Thu May 31 2012 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.3.0-1
- Update to 3.3.0

* Wed May 9 2012 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.2.6-2
- Add BuildRequires: libxml2-devel, BZ 819916

* Wed Mar 21 2012 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.2.6-1
- Update to 3.2.6

* Thu Feb 16 2012 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.2.5-8
- rename patch files

* Mon Jan 16 2012 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.2.5-7
- patch configure.ac to compile -O2 instead of -O0 on Linux.

* Tue Jan 10 2012 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.2.5-6
- glusterd.init use /run per Fedora File System Layout, or /var/run when
  needed

* Tue Jan 3 2012 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.2.5-5
- revised spec for init.d for fedora<=16, rhel<=6; native systemd for
  f17 and rhel7

* Wed Dec 7 2011 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.2.5-4
- revised sysconfig and init.d scripts. (glusterfsd.{init,sysconfig,service}
  should go away, as glusterd is responsible for starting and stopping it.)

* Wed Nov 23 2011 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.2.5-3
- revised libglusterfs/src/Makefile.* to (re)enable parallel make

* Mon Nov 21 2011 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.2.5-2
- rhel/epel, init.d for <=6, native systemd for 7

* Thu Nov 17 2011 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.2.5-1
- Update to 3.2.5

* Wed Nov 16 2011 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.2.4-3
- revised init.d/systemd to minimize fedora < 17
- get closer to the official glusterfs spec, including...
- add geo-replication, which should have been there since 3.2

* Wed Nov 2 2011 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.2.4-2
- Convert init.d to systemd for f17 and later

* Fri Sep 30 2011 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.2.4-1
- Update to 3.2.4

* Mon Aug 22 2011 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.2.3-1
- Update to 3.2.3

* Mon Aug 22 2011 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.2.2-1
- Update to 3.2.2

* Fri Aug 19 2011 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 3.2.2-0
- Update to 3.2.2

* Wed Jun 29 2011 Dan Horák <dan[at]danny.cz> - 3.2.1-3
- disable InfiniBand on s390(x) unconditionally

* Thu Jun 16 2011 Jonathan Steffan <jsteffan@fedoraproject.org> - 3.2.1-2
- Fix Source0 URL

* Thu Jun 16 2011 Jonathan Steffan <jsteffan@fedoraproject.org> - 3.2.1-1
- Update to 3.2.1

* Wed Jun 01 2011 Jonathan Steffan <jsteffan@fedoraproject.org> - 3.2.0-1
- Update to 3.2.0

* Tue May 10 2011 Jonathan Steffan <jsteffan@fedoraproject.org> - 3.1.4-1
- Update to 3.1.4

* Sat Mar 19 2011 Jonathan Steffan <jsteffan@fedoraproject.org> - 3.1.3-1
- Update to 3.1.3
- Merge in more upstream SPEC changes
- Remove patches from GlusterFS bugzilla #2309 and #2311
- Remove inode-gen.patch

* Sun Feb 06 2011 Jonathan Steffan <jsteffan@fedoraproject.org> - 3.1.2-3
- Add back in legacy SPEC elements to support older branches

* Thu Feb 03 2011 Jonathan Steffan <jsteffan@fedoraproject.org> - 3.1.2-2
- Add patches from CloudFS project

* Tue Jan 25 2011 Jonathan Steffan <jsteffan@fedoraproject.org> - 3.1.2-1
- Update to 3.1.2

* Wed Jan 5 2011 Dan Horák <dan[at]danny.cz> - 3.1.1-3
- no InfiniBand on s390(x)

* Sat Jan 1 2011 Jonathan Steffan <jsteffan@fedoraproject.org> - 3.1.1-2
- Update to support readline
- Update to not parallel build

* Mon Dec 27 2010 Silas Sewell <silas@sewell.ch> - 3.1.1-1
- Update to 3.1.1
- Change package names to mirror upstream

* Mon Dec 20 2010 Jonathan Steffan <jsteffan@fedoraproject.org> - 3.0.7-1
- Update to 3.0.7

* Wed Jul 28 2010 Jonathan Steffan <jsteffan@fedoraproject.org> - 3.0.5-1
- Update to 3.0.x

* Sat Apr 10 2010 Jonathan Steffan <jsteffan@fedoraproject.org> - 2.0.9-2
- Move python version requires into a proper BuildRequires otherwise
  the spec always turned off python bindings as python is not part
  of buildsys-build and the chroot will never have python unless we
  require it
- Temporarily set -D_FORTIFY_SOURCE=1 until upstream fixes code
  GlusterFS Bugzilla #197 (#555728)
- Move glusterfs-volgen to devel subpackage (#555724)
- Update description (#554947)

* Sat Jan 2 2010 Jonathan Steffan <jsteffan@fedoraproject.org> - 2.0.9-1
- Update to 2.0.9

* Sun Nov 8 2009 Jonathan Steffan <jsteffan@fedoraproject.org> - 2.0.8-1
- Update to 2.0.8
- Remove install of glusterfs-volgen, it's properly added to
  automake upstream now

* Sat Oct 31 2009 Jonathan Steffan <jsteffan@fedoraproject.org> - 2.0.7-1
- Update to 2.0.7
- Install glusterfs-volgen, until it's properly added to automake
  by upstream
- Add macro to be able to ship more docs

* Thu Sep 17 2009 Peter Lemenkov <lemenkov@gmail.com> 2.0.6-2
- Rebuilt with new fuse

* Sat Sep 12 2009 Matthias Saou <http://freshrpms.net/> 2.0.6-1
- Update to 2.0.6.
- No longer default to disable the client on RHEL5 (#522192).
- Update spec file URLs.

* Mon Jul 27 2009 Matthias Saou <http://freshrpms.net/> 2.0.4-1
- Update to 2.0.4.

* Thu Jun 11 2009 Matthias Saou <http://freshrpms.net/> 2.0.1-2
- Remove libglusterfs/src/y.tab.c to fix koji F11/devel builds.

* Sat May 16 2009 Matthias Saou <http://freshrpms.net/> 2.0.1-1
- Update to 2.0.1.

* Thu May  7 2009 Matthias Saou <http://freshrpms.net/> 2.0.0-1
- Update to 2.0.0 final.

* Wed Apr 29 2009 Matthias Saou <http://freshrpms.net/> 2.0.0-0.3.rc8
- Move glusterfsd to common, since the client has a symlink to it.

* Fri Apr 24 2009 Matthias Saou <http://freshrpms.net/> 2.0.0-0.2.rc8
- Update to 2.0.0rc8.

* Sun Apr 12 2009 Matthias Saou <http://freshrpms.net/> 2.0.0-0.2.rc7
- Update glusterfsd init script to the new style init.
- Update files to match the new default vol file names.
- Include logrotate for glusterfsd, use a pid file by default.
- Include logrotate for glusterfs, using killall for lack of anything better.

* Sat Apr 11 2009 Matthias Saou <http://freshrpms.net/> 2.0.0-0.1.rc7
- Update to 2.0.0rc7.
- Rename "libs" to "common" and move the binary, man page and log dir there.

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 16 2009 Matthias Saou <http://freshrpms.net/> 2.0.0-0.1.rc1
- Update to 2.0.0rc1.
- Include new libglusterfsclient.h.

* Mon Feb 16 2009 Matthias Saou <http://freshrpms.net/> 1.3.12-1
- Update to 1.3.12.
- Remove no longer needed ocreat patch.

* Thu Jul 17 2008 Matthias Saou <http://freshrpms.net/> 1.3.10-1
- Update to 1.3.10.
- Remove mount patch, it's been included upstream now.

* Fri May 16 2008 Matthias Saou <http://freshrpms.net/> 1.3.9-1
- Update to 1.3.9.

* Fri May  9 2008 Matthias Saou <http://freshrpms.net/> 1.3.8-1
- Update to 1.3.8 final.

* Wed Apr 23 2008 Matthias Saou <http://freshrpms.net/> 1.3.8-0.10
- Include short patch to include fixes from latest TLA 751.

* Tue Apr 22 2008 Matthias Saou <http://freshrpms.net/> 1.3.8-0.9
- Update to 1.3.8pre6.
- Include glusterfs binary in both the client and server packages, now that
  glusterfsd is a symlink to it instead of a separate binary.

* Sun Feb  3 2008 Matthias Saou <http://freshrpms.net/> 1.3.8-0.8
- Add python version check and disable bindings for version < 2.4.

* Sun Feb  3 2008 Matthias Saou <http://freshrpms.net/> 1.3.8-0.7
- Add --without client rpmbuild option, make it the default for RHEL (no fuse).
  (I hope "rhel" is the proper default macro name, couldn't find it...)

* Wed Jan 30 2008 Matthias Saou <http://freshrpms.net/> 1.3.8-0.6
- Add --without ibverbs rpmbuild option to the package.

* Mon Jan 14 2008 Matthias Saou <http://freshrpms.net/> 1.3.8-0.5
- Update to current TLA again, patch-636 which fixes the known segfaults.

* Thu Jan 10 2008 Matthias Saou <http://freshrpms.net/> 1.3.8-0.4
- Downgrade to glusterfs--mainline--2.5--patch-628 which is more stable.

* Tue Jan  8 2008 Matthias Saou <http://freshrpms.net/> 1.3.8-0.3
- Update to current TLA snapshot.
- Include umount.glusterfs wrapper script (really needed? dunno).
- Include patch to mount wrapper to avoid multiple identical mounts.

* Sun Dec 30 2007 Matthias Saou <http://freshrpms.net/> 1.3.8-0.1
- Update to current TLA snapshot, which includes "volume-name=" fstab option.

* Mon Dec  3 2007 Matthias Saou <http://freshrpms.net/> 1.3.7-6
- Re-add the /var/log/glusterfs directory in the client sub-package (required).
- Include custom patch to support vol= in fstab for -n glusterfs client option.

* Mon Nov 26 2007 Matthias Saou <http://freshrpms.net/> 1.3.7-4
- Re-enable libibverbs.
- Check and update License field to GPLv3+.
- Add glusterfs-common obsoletes, to provide upgrade path from old packages.
- Include patch to add mode to O_CREATE opens.

* Thu Nov 22 2007 Matthias Saou <http://freshrpms.net/> 1.3.7-3
- Remove Makefile* files from examples.
- Include RHEL/Fedora type init script, since the included ones don't do.

* Wed Nov 21 2007 Matthias Saou <http://freshrpms.net/> 1.3.7-1
- Major spec file cleanup.
- Add missing %%clean section.
- Fix ldconfig calls (weren't set for the proper sub-package).

* Sat Aug 4 2007 Matt Paine <matt@mattsoftware.com> - 1.3.pre7
- Added support to build rpm without ibverbs support (use --without ibverbs
  switch)

* Sun Jul 15 2007 Matt Paine <matt@mattsoftware.com> - 1.3.pre6
- Initial spec file
