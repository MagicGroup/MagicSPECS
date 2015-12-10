%global gem_name em-socksify

Name: rubygem-%{gem_name}
Version: 0.3.0
Release: 12%{?dist}
Summary: Transparent proxy support for any EventMachine protocol
Group: Development/Languages
License: MIT
URL: https://github.com/igrigorik/em-socksify
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
Source1: MIT-LICENSE
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildArch: noarch
%if 0%{?fc19} || 0%{?fc20}
Requires: ruby(release)
Requires: rubygems
Requires: rubygem(eventmachine) >= 1.0.0.beta.4
Provides: rubygem(%{gem_name}) = %{version}
%endif


%description
Transparent proxy support for any EventMachine protocol

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
cp -p %{SOURCE1} %{buildroot}/%{gem_instdir}/

#Spec suite only includes 2 tests that require external connections,
#commented out since this isn't possible within mock
#%%check
#pushd ./%%{gem_instdir}
#rspec -Ilib spec
#popd

%files
%dir %{gem_instdir}
%exclude %{gem_cache}
%exclude %{gem_instdir}/.gitignore
%{gem_spec}
%doc %{gem_instdir}/MIT-LICENSE
%{gem_libdir}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md
%{gem_instdir}/spec
%{gem_instdir}/Gemfile
%{gem_instdir}/Rakefile
%{gem_instdir}/em-socksify.gemspec

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 0.3.0-12
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.3.0-11
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.3.0-10
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild


* Wed May 28 2014 Nitesh Narayan Lal <niteshnarayan@fedoraproject.org> - 0.3.0-8
- Added conditional for F19/F20 and marked readme as doc

* Fri Mar 28 2014 Nitesh Narayan Lal <niteshnarayan@fedoraproject.org> - 0.3.0-7
- Fixing licensing issues

* Tue Mar 25 2014 Nitesh Narayan Lal <niteshnarayan@fedoraproject.org> - 0.3.0-6
- Updating licensing  & other issues so as to comply with Fedora guidelines

* Sat Mar 15 2014 Nitesh Narayan Lal <niteshnarayan@fedoraproject.org> - 0.3.0-5
- Correcting missing requirements & updating as per the Fedora guidelines

* Sat Mar 15 2014 Nitesh Narayan Lal <niteshnarayan@fedoraproject.org> - 0.3.0-4
- Updated to comply with Fedora guidelines

* Thu Mar 6 2014 Nitesh Narayan Lal <niteshnarayan@fedoraproject.org> - 0.3.0-3
- Updated as per the Fedora usage guidelines

* Sat Feb 22 2014 Nitesh Narayan Lal <niteshnarayan@fedoraproject.org>  0.3.0-2
- Updated as per the comments

* Sat Jan 11 2014 Nitesh Narayan Lal <niteshnarayan@fedoraproject.org>  0.3.0-1
- Initial package
