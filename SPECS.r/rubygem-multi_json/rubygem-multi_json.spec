# Generated from multi_json-1.0.3.gem by gem2rpm -*- rpm-spec -*-
%global gem_name multi_json

Name: rubygem-%{gem_name}
Version: 1.10.1
Release: 4%{?dist}
Summary: A common interface to multiple JSON libraries
Group: Development/Languages
License: MIT
URL: http://github.com/intridea/multi_json
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel >= 1.3.6
BuildRequires: ruby
BuildRequires: rubygem(rspec)
#BuildRequires: rubygem(json)
BuildRequires: rubygem(json_pure)
BuildArch: noarch
# OkJson is allowed to be bundled:
# https://fedorahosted.org/fpc/ticket/113
Provides: bundled(okjson) = 43

%description
A common interface to multiple JSON libraries, including Oj, Yajl, the JSON
gem (with C-extensions), the pure-Ruby JSON gem, NSJSONSerialization, gson.rb,
JrJackson, and OkJson.


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

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
# oj is not available on Fedora.
sed -i '139,164 s/^/#/' spec/multi_json_spec.rb
sed -i "/expect(MultiJson.adapter.to_s).to eq('MultiJson::Adapters::Oj')/ s/Oj/JsonGem/" spec/multi_json_spec.rb

# Execute main test suite.
rspec spec/multi_json_spec.rb

# Disable test of engines unsupported on Fedora (they may cause test suite to
# exit).
rm spec/{gson,jr_jackson,nsjsonserialization,oj,yajl}_adapter_spec.rb

# Adapters have to be tested separately.
for adapter in spec/*_adapter_spec.rb; do
  rspec $adapter
done

popd

%files
%dir %{gem_instdir}
%exclude %{gem_instdir}/.*
%exclude %{gem_instdir}/Gemfile
%exclude %{gem_instdir}/%{gem_name}.gemspec
%doc %{gem_instdir}/LICENSE.md
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/CONTRIBUTING.md
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/spec


%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.10.1-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.10.1-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Mar 02 2015 Vít Ondruch <vondruch@redhat.com> - 1.10.1-1
- Update to MultiJSON 1.10.1.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Feb 12 2014 Vít Ondruch <vondruch@redhat.com> - 1.8.4-1
- Update to multi_json 1.8.4.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 14 2013 Vít Ondruch <vondruch@redhat.com> - 1.7.7-1
- Update to multi_json 1.7.7.

* Wed Mar 20 2013 Vít Ondruch <vondruch@redhat.com> - 1.7.1-1
- Update to multi_json 1.7.1.

* Tue Feb 26 2013 Vít Ondruch <vondruch@redhat.com> - 1.3.6-4
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.3.6-1
- Update to multi_json 1.3.6.
- Switch to rubygem(rspec) from rubygem(rspec-core).

* Tue Jan 24 2012 Vít Ondruch <vondruch@redhat.com> - 1.0.3-5
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 11 2011 Vít Ondruch <vondruch@redhat.com> - 1.0.3-3
- Removed useless shebang.

* Fri Nov 11 2011 Vít Ondruch <vondruch@redhat.com> - 1.0.3-2
- Review fixes.

* Fri Jul 08 2011 Vít Ondruch <vondruch@redhat.com> - 1.0.3-1
- Initial package
