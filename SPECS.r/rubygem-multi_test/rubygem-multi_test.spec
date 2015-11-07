%global gem_name multi_test

Name: rubygem-%{gem_name}
Version: 0.1.1
Release: 4%{?dist}
Summary: Wafter-thin gem to disable autorun of various testing libraries
Group: Development/Languages
License: MIT
URL: http://cukes.info
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildArch: noarch

%description
multi_test gives a uniform interface onto whatever testing library has been
loaded into a running Ruby process. It can be used to clobber autorun behaviour
from older versions of Test::Unit that automatically hook in when the user
requires them.


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}

%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
gem build %{gem_name}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
# Unfortunatelly tests depend heavily on Bundler
# and testing different versions of gems
#. test/all
popd

%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%exclude %{gem_instdir}/.travis.yml
%{gem_spec}
%doc %{gem_instdir}/LICENSE

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/History.md
%{gem_instdir}/Makefile
%{gem_instdir}/Rakefile
%{gem_instdir}/test
%{gem_instdir}/%{gem_name}.gemspec

%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 0.1.1-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.1.1-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 18 2014 Josef Stribny <jstribny@redhat.com> - 0.1.1-1
- Initial package
