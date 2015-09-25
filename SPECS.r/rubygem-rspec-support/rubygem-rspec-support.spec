%global	gem_name	rspec-support

%global	mainver	3.3.0
%undefine	prever

%global	mainrel	2
%global	prerpmver	%(echo "%{?prever}" | sed -e 's|\\.||g')

%global	need_bootstrap_set	0

Name:		rubygem-%{gem_name}
Version:	%{mainver}
Release:	%{?prever:0.}%{mainrel}%{?prever:.%{prerpmver}}%{?dist}.1

Summary:	Common functionality to Rspec series
Group:		Development/Languages
License:	MIT
URL:		https://github.com/rspec/rspec-support
Source0:	https://rubygems.org/gems/%{gem_name}-%{mainver}%{?prever}.gem
# %%{SOURCE2} %%{name} %%{version} 
Source1:	rubygem-%{gem_name}-%{version}-full.tar.gz
Source2:	rspec-related-create-full-tarball.sh
# tweak regex for search path
Patch0:	rubygem-rspec-support-3.2.1-callerfilter-searchpath-regex.patch

BuildRequires:	ruby(release)
BuildRequires:	rubygems-devel
%if 0%{?need_bootstrap_set} < 1
BuildRequires:	rubygem(rspec)
BuildRequires:	git
%endif

BuildArch:		noarch
# Need fix
Provides:		rubygem(%{gem_name}) = %{version}-%{release}

%description
`RSpec::Support` provides common functionality to `RSpec::Core`,
`RSpec::Expectations` and `RSpec::Mocks`. It is considered
suitable for internal use only at this time.

%package	doc
Summary:	Documentation for %{name}
Group:		Documentation
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description	doc
Documentation for %{name}

%global	version_orig	%{version}
%global	version	%{version_orig}%{?prever}

%prep
gem unpack %{SOURCE0}
%setup -q -D -T -n  %{gem_name}-%{version} -a 1
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

( 
cd %{gem_name}-%{version}
%patch0 -p1
)

%build
gem build %{gem_name}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
	%{buildroot}%{gem_dir}/

%if 0%{?need_bootstrap_set} < 1
%check
LANG=en_US.UTF-8
pushd %{gem_name}-%{version}

ruby -rubygems -Ilib/ -S rspec spec/

popd
%endif

%files
%dir	%{gem_instdir}
%doc	%{gem_instdir}/Changelog.md
%doc	%{gem_instdir}/README.md
%license	%{gem_instdir}/LICENSE.txt

%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc	%{gem_docdir}

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 3.3.0-2.1
- 为 Magic 3.0 重建

* Sun Aug  2 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.3.0-2
- Enable tests again

* Sun Aug  2 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.3.0-1
- 3.3.0
- Once disable tests

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.2-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Feb 25 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.2.2-1
- 3.2.2

* Mon Feb  9 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.2.1-2
- Enable tests again

* Mon Feb  9 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.2.1-1
- 3.2.1
- Once disable tests

* Mon Nov 10 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.1.2-3
- Enable tests again

* Mon Nov 10 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.1.2-2
- Retry

* Mon Nov 10 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.1.2-1
- 3.1.2
- Once disable tests

* Fri Aug 15 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.0.4-1
- 3.0.4

* Thu Aug 14 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.0.3-1
- 3.0.3

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.0-0.4.beta2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 18 2014 Mamoru TASAKA <mtasaka@tbz.t-com.ne.jp> - 3.0.0-0.4.beta1
- 3.0.0 beta 2

* Mon Feb 10 2014 Mamoru TASAKA <mtasaka@tbz.t-com.ne.jp> - 3.0.0-0.2.beta1
- Modify Provides EVR

* Mon Feb 03 2014 Mamoru TASAKA <mtasaka@tbz.t-com.ne.jp> - 3.0.0-0.1.beta1
- Initial package
