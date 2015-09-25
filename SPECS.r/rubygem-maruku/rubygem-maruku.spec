%define gem_name maruku

Name: rubygem-%{gem_name}
Version: 0.7.2
Release: 2%{?dist}
Summary: Maruku is a Markdown-superset interpreter written in Ruby
Group: Development/Languages
# lib/maruku/ext/fenced_code.rb - BSD
License: MIT and BSD
URL: http://github.com/bhollis/maruku
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(rspec)
BuildArch: noarch

%description
Maruku is a Markdown interpreter in Ruby. It features native export to HTML
and PDF (via Latex). The output is really beautiful!


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
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


mkdir -p %{buildroot}%{_bindir}
cp -a .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

# Run the test suite
%check
pushd .%{gem_instdir}
# We don't care about coveraga.
sed -i '/[Ss]imple[Cc]ov/ s/^/#/' spec/spec_helper.rb

# We don't have nokogiri-diff in Fedora yet.
mv spec/block_spec.rb{,.disable}

rspec spec
popd

%files
%dir %{gem_instdir}
%{_bindir}/maruku
%{_bindir}/marutex
%license %{gem_instdir}/MIT-LICENSE.txt
%{gem_instdir}/bin
%{gem_instdir}/data
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/docs
%{gem_instdir}/spec

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.7.2-2
- 为 Magic 3.0 重建

* Tue Sep 15 2015 Vít Ondruch <vondruch@redhat.com> - 0.7.2-1
- Update to Maruku 0.7.2.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 19 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.6.0-10
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jan 31 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.6.0-7
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Aug 08 2011 Mo Morsi <mmorsi@redhat.com> - 0.6.0-5
- Replace BR(check) with BR

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb 23 2010 Mohammed Morsi <mmorsi@redhat.com> - 0.6.0-3
- added geminstdir to file list
- added rubygem(rake) dependency
- other fixes to conform to package guidelines

* Mon Feb 08 2010 Mohammed Morsi <mmorsi@redhat.com> - 0.6.0-2
- cleaned up macros, other package guideline compliance fixes
- corrected license
- include all files and docs, added check/test section

* Mon Feb 08 2010 Mohammed Morsi <mmorsi@redhat.com> - 0.6.0-1
- Initial package
