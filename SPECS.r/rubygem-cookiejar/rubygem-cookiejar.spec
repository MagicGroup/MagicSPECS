%global gem_name cookiejar	

Name: rubygem-%{gem_name}
Version: 0.3.2
Release: 7%{?dist}
Summary: Parsing and returning cookies in Ruby
Group: Development/Languages
License: BSD	
URL: https://github.com/dwaite/cookiejar
Source0: https://rubygems.org/gems/cookiejar-%{version}.gem
BuildRequires: rubygem(rspec)
BuildRequires: ruby(release)
BuildRequires: rubygems-devel 
BuildArch: noarch
%if 0%{?fc19} || 0%{?fc20}
Requires: ruby(release)
Requires: rubygems
Provides: rubygem(%{gem_name}) = %{version}
%endif

%description
The Ruby CookieJar is a library to help manage client-side cookies in pure
Ruby. It enables parsing and setting of cookie headers, alternating between
multiple 'jars' of cookies at one time (such as having a set of cookies for
each browser or thread), and supports persistence of the cookies in a JSON
string.

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


%check
pushd ./%{gem_instdir}
rspec -Ilib spec
popd	

%install

mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%exclude %{gem_instdir}/contributors.json
%{gem_spec}
%doc %{gem_instdir}/spec/*
%doc %{gem_instdir}/LICENSE

%files doc
%{gem_docdir}  
%{gem_instdir}/README.markdown
%{gem_instdir}/Rakefile

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.3.2-7
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.3.2-6
- 为 Magic 3.0 重建


* Tue Jun 24 2014 Nitesh Narayan Lal <niteshnarayan@fedoraproject.org> - 0.3.2-5
- Updated to latest upstream release

* Wed May 28 2014 Nitesh Narayan Lal <niteshnarayan@fedoraproject.org> - 0.3.2-4
- Added conditional for F19/F20

* Sat Mar 15 2014 Nitesh Narayan Lal <niteshnarayan@fedoraproject.org> - 0.3.2-3
- Updated to comply with Fedora guidelines

* Thu Mar 6 2014 Nitesh Narayan Lal <niteshnarayan@fedoraproject.org> - 0.3.2-2
- Updated as per the Fedora guidelines

* Sat Jan 11 2014 Nitesh Narayan Lal <niteshnarayan@fedoraproject.org> - 0.3.2-1
- Initial package
