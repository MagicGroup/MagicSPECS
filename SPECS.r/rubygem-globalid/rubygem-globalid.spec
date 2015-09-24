# Generated from globalid-0.3.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name globalid

Name: rubygem-%{gem_name}
Version: 0.3.3
Release: 2%{?dist}
Summary: Refer to any model with a URI: gid://app/class/id
Group: Development/Languages
License: MIT
URL: http://www.rubyonrails.org
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone https://github.com/rails/globalid.git && cd globalid
# git checkout v0.3.0
# tar czvf globalid-0.3.3-tests.tar.gz test/
Source1: globalid-0.3.3-tests.tar.gz
BuildRequires: ruby(release)
BuildRequires: rubygems-devel 
BuildRequires: ruby >= 1.9.3
BuildRequires: rubygem(activesupport) >= 4.1
BuildRequires: rubygem(activemodel) >= 4.1
BuildRequires: rubygem(railties) >= 4.1
BuildArch: noarch

%description
URIs for your models makes it easy to pass references around.


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
gem build %{gem_name}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


%check
pushd .%{gem_instdir}
tar xf %{SOURCE1}
sed -i '1d' ./test/helper.rb
ruby -Ilib:test -rforwardable -e "Dir.glob './test/cases/*test.rb', &method(:require)"
popd


%files
%dir %{gem_instdir}
%{gem_libdir}
%license %{gem_instdir}/MIT-LICENSE
%{gem_instdir}/lib
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Mar 19 2015 Josef Stribny <jstribny@redhat.com> - 0.3.3-1
- Update to 0.3.3

* Tue Jan 06 2015 Josef Stribny <jstribny@redhat.com> - 0.3.0-1
- Initial package
