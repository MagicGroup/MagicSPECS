# Generated from CFPropertyList-2.3.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name CFPropertyList

Name: rubygem-%{gem_name}
Version: 2.3.0
Release: 2%{?dist}
Summary: Read, write and manipulate property lists as defined by Apple
Group: Development/Languages
License: MIT
URL: http://github.com/ckruse/CFPropertyList
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone https://github.com/ckruse/CFPropertyList.git && cd CFPropertyList && git checkout cfpropertyList-2.3.0
# tar czvf CFPropertyList-2.3.0-tests.tgz test/
Source1: %{gem_name}-%{version}-tests.tgz
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(nokogiri)
BuildArch: noarch

%description
This is a module to read, write and manipulate both binary and XML property
lists as defined by apple.


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
tar xzvf %{SOURCE1}

# We don't have rubygem-libxml-ruby in Fedora.
sed -i '/_libxml/,/^  end$/ s/^/#/' test/test_*.rb

ruby -Ilib:test -e 'Dir.glob "./test/**/test_*.rb", &method(:require)'
popd

%files
%dir %{gem_instdir}
%doc %{gem_instdir}/README
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Mar 19 2015 Vít Ondruch <vondruch@redhat.com> - 2.3.0-1
- Initial package
