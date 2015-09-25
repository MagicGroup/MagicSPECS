# Generated from rubeyond-0.1.gem by gem2rpm -*- rpm-spec -*-
%global gem_name rubeyond
%global rubyabi 1.9.1

Summary:       A development framework for Ruby
Name:          rubygem-%{gem_name}
Version:       0.1
Release:       5.1%{?dist}
License:       GPLv3+

URL:           http://rubyforge.org/projects/rubeyond
Source0:       http://rubygems.org/gems/%{gem_name}-%{version}.gem

%if 0%{?fedora} >= 19
BuildRequires: ruby(release)
%else
BuildRequires: ruby(abi) = %{rubyabi}
BuildRequires: ruby
%endif
BuildRequires: rubygems-devel

BuildArch:     noarch

%if 0%{?fedora} >= 19
Requires:      ruby(release)
%else
Requires:      ruby(abi) = %{rubyabi}
Requires:      ruby
%endif

Requires:      rubygems

Provides:      rubygem(%{gem_name}) = %{version}

%description
Rubeyond provides addition general classes, mixins and
functions to round out the standard library that ships
with the Ruby language.


%package doc
Summary:   Documentation for %{name}
Group:     Documentation
Requires:  %{name} = %{version}-%{release}
BuildArch: noarch


%description doc
Documentation for %{name}


%prep
gem unpack %{SOURCE0}
%setup -q -D -T -n %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

# apply any patches here


%build
gem build %{gem_name}.gemspec

%gem_install


%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}
%doc %{gem_instdir}/LICENSE
%doc %{gem_instdir}/TODO
%doc %{gem_instdir}/ChangeLog

%files doc
%doc %{gem_docdir}

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.1-5.1
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-4.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 28 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.1-1.1
- First build for Fedora.
- Resolves: BZ#915331
- Fixed license to be GPLv3+.
- Create the gem_dir before the install.
- Added macros for building on f19+.

* Mon Feb 25 2013 Darryl L. Pierce <dpierce@redhat.com> - 0.1-1
- Initial package
