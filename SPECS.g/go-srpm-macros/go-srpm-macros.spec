Name:           go-srpm-macros
Version:        2
Release:        4%{?dist}
Summary:        RPM macros for building Golang packages for various architectures
Summary(zh_CN.UTF-8): 构建 Golang 包需要的 RPM 宏
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License:        GPLv3+
Source0:        macros.go-srpm
BuildArch:      noarch
# for install command
BuildRequires:  coreutils

%description
The package provides macros for building projects in Go
on various architectures.

%description -l zh_CN.UTF-8
构建 Golang 包需要的 RPM 宏。

%prep
# nothing to prep, just for hooks

%build
# nothing to build, just for hooks

%install
install -m 644 -D "%{SOURCE0}" \
    '%{buildroot}%{_rpmconfigdir}/macros.d/macros.go-srpm'

%files
%{_rpmconfigdir}/macros.d/macros.go-srpm

%changelog
* Tue Dec 08 2015 Liu Di <liudidi@gmail.com> - 2-4
- 为 Magic 3.0 重建

* Thu Sep 10 2015 jchaloup <jchaloup@redhat.com> - 2-3
- Remove compiler specific macros (moved to go-compiler package)
- Define go-compiler macro to signal go-compiler packages is available

* Sat Aug 29 2015 jchaloup <jchaloup@redhat.com> - 2-2
- Add -ldflags $LDFLAGS to go build/test macro

* Sun Aug 23 2015 Peter Robinson <pbrobinson@fedoraproject.org> 2-1
- aarch64 now has golang

* Tue Jul 07 2015 jchaloup <jchaloup@redhat.com> - 1-1
- Initial commit
  resolves: #1241156
