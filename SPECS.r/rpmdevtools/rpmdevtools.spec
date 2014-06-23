%global spectool_version 1.0.10

Name:           rpmdevtools
Version:	8.4
Release:        3%{?dist}
Summary:        RPM Development Tools
Summary(zh_CN.UTF-8): RPM 开发工具

# rpmdev-setuptree is GPLv2, everything else GPLv2+
License:        GPLv2+ and GPLv2
URL:            https://fedorahosted.org/rpmdevtools/
Source0:        https://fedorahosted.org/released/rpmdevtools/%{name}-%{version}.tar.xz

# 允许不更新 Release 号，以便进行版本更新
Patch0:		rpmdevtools-8.4-allownobump.patch

BuildArch:      noarch
# help2man, pod2man, *python for creating man pages
BuildRequires:  help2man
BuildRequires:  %{_bindir}/pod2man
BuildRequires:  python >= 2.4
BuildRequires:  rpm-python
# emacs-common >= 1:22.3-3 for macros.emacs
BuildRequires:  emacs-common >= 1:22.3-3
%if 0%{?fedora}
# xemacs-common >= 21.5.29-8 for macros.xemacs
BuildRequires:  xemacs-common >= 21.5.29-8
%endif
Provides:       spectool = %{spectool_version}
Requires:       curl
Requires:       diffutils
Requires:       fakeroot
Requires:       file
Requires:       findutils
Requires:       gawk
Requires:       grep
Requires:       %{_bindir}/man
Requires:       python >= 2.4
Requires:       rpm-build >= 4.4.2.3
Requires:       rpm-python
Requires:       sed
Requires:       emacs-filesystem
%if 0%{?fedora}
Requires:       xemacs-filesystem
%endif

%description
This package contains scripts and (X)Emacs support files to aid in
development of RPM packages.
rpmdev-setuptree    Create RPM build tree within user's home directory
rpmdev-diff         Diff contents of two archives
rpmdev-newspec      Creates new .spec from template
rpmdev-rmdevelrpms  Find (and optionally remove) "development" RPMs
rpmdev-checksig     Check package signatures using alternate RPM keyring
rpminfo             Print information about executables and libraries
rpmdev-md5/sha*     Display checksums of all files in an archive file
rpmdev-vercmp       RPM version comparison checker
spectool            Expand and download sources and patches in specfiles
rpmdev-wipetree     Erase all files within dirs created by rpmdev-setuptree
rpmdev-extract      Extract various archives, "tar xvf" style
rpmdev-bumpspec     Bump revision in specfile
...and many more.

%description -l zh_CN.UTF-8
这个包包含了为了开发 RPM 而制作的脚本和 (X)Emacs 支持文件。
rpmdev-setuptree    在用户目录下新建 RPM 构建树
rpmdev-diff	    比较两个文档的差异
rpmdev-newspec	    从模板中新建 .spec
rpmdev-rmdevelrpms  查找（并可选删除）"开发包" RPM
rpmdev-checksig     检查 RPM 包签名
rpminfo		    打印可执行程序和库信息
rpmdev-md5/sha*     显示文档中所有文件的校验和
rpmdev-vercmp	    比较 RPM 的版本
spectool	    解析并下载 spec 文件中的源代码和补丁
rpmdev-wipetree     删除由 rpmdev-setuptree 建立的目录和文件
rpmdev-extract      解压多种文件，"tar xvf" 风格
rpmdev-bumpspec     修改 spec 文件中的版本号
...等等。

%prep
%setup -q
%patch0 -p1

%build
%configure --libdir=%{_prefix}/lib
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

%if 0%{?fedora}
for dir in %{_emacs_sitestartdir} %{_xemacs_sitestartdir} ; do
%else
for dir in %{_emacs_sitestartdir} ; do
%endif
  install -dm 755 $RPM_BUILD_ROOT$dir
  ln -s %{_datadir}/rpmdevtools/rpmdev-init.el $RPM_BUILD_ROOT$dir
  touch $RPM_BUILD_ROOT$dir/rpmdev-init.elc
done


%files
%doc COPYING NEWS
%config(noreplace) %{_sysconfdir}/rpmdevtools/
%{_sysconfdir}/bash_completion.d/
%{_datadir}/rpmdevtools/
%{_bindir}/*
%{_emacs_sitestartdir}/rpmdev-init.el
%ghost %{_emacs_sitestartdir}/rpmdev-init.elc
%if 0%{?fedora}
%{_xemacs_sitestartdir}/rpmdev-init.el
%ghost %{_xemacs_sitestartdir}/rpmdev-init.elc
%endif
%{_mandir}/man[18]/*.[18]*


%changelog
* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 8.4-3
- 为 Magic 3.0 重建

* Wed Feb 26 2014 Liu Di <liudidi@gmail.com> - 8.4-2
- 更新到 8.4

* Wed Feb 26 2014 Liu Di <liudidi@gmail.com> - 8.4-2
- 更新到 rpmdevtools
