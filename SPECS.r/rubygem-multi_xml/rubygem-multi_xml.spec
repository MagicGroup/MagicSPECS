# Generated from multi_xml-0.4.1.gem by gem2rpm -*- rpm-spec -*-
%global gem_name multi_xml

Summary: A generic swappable back-end for XML parsing
Name: rubygem-%{gem_name}
Version: 0.5.5
Release: 2%{?dist}
Group: Development/Languages
License: MIT
URL: https://github.com/sferik/multi_xml
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# RSpec 3.x fixes.
# https://github.com/sferik/multi_xml/commit/a4ae6aa9810ab44634df977f9d0d37efb785c45c
Patch0: rubygem-multi_xml-0.5.5-Prepare-for-rspec-3-0.patch
BuildRequires: ruby
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: rubygem(rspec)
BuildRequires: rubygem(nokogiri)
# rubygem-ox is not yet in Fedora.
# https://bugzilla.redhat.com/show_bug.cgi?id=1142491
# BuildRequires: rubygem(ox)
BuildArch: noarch

%description
A gem to provide swappable XML backends utilizing LibXML, Nokogiri, Ox, or
REXML.


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.


%prep
%setup -q -c -T
%gem_install -n %{SOURCE0}

pushd .%{gem_instdir}
%patch0 -p1
popd

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/



%check
pushd .%{gem_instdir}
# We don't care about code coverage.
sed -i '/simplecov/,/SimpleCov\.start/ s/^/#/' spec/helper.rb

# Ox is the most prefered XML parser by MultiXML. This would succeed if there
# were Ox in Fedora.
sed -i "/expect(MultiXml\.parser\.name)\.to eq('MultiXml::Parsers::Ox')/ s/Ox/Nokogiri/" \
  spec/multi_xml_spec.rb

rspec spec
popd

%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_instdir}/.*
%exclude %{gem_cache}
%{gem_spec}
%doc %{gem_instdir}/README.md
%license %{gem_instdir}/LICENSE.md


%files doc
%doc %{gem_docdir}
%{gem_instdir}/spec
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/CONTRIBUTING.md
%{gem_instdir}/Rakefile
%{gem_instdir}/*.gemspec


%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Feb 24 2015 Vít Ondruch <vondruch@redhat.com> - 0.5.5-1
- Update to MultiXML 0.5.5.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 04 2013 Vít Ondruch <vondruch@redhat.com> - 0.5.2-3
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 14 2013 Vít Ondruch <vondruch@redhat.com> - 0.5.2-1
- Update to multi_xml 0.5.2.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Mar 02 2012 Vít Ondruch <vondruch@redhat.com> - 0.4.1-3
- Update review.

* Mon Feb 20 2012 Michael Stahnke <stahnma@fedoraproject.org> - 0.4.1-2
- Update review

* Fri Jan 20 2012 Michael Stahnke <mastahnke@gmail.com> - 0.4.1-1
- Initial package
