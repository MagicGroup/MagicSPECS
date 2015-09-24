%global gem_name arel

Summary: Arel is a Relational Algebra for Ruby
Name: rubygem-%{gem_name}
Version: 6.0.3
Release: 1%{?dist}
Group: Development/Languages
License: MIT
URL: http://github.com/rails/%{gem_name}
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone https://github.com/rails/arel.git && cd arel
# git checkout v6.0.3 && tar czvf arel-6.0.3-tests.tgz ./test/
Source1: arel-%{version}-tests.tgz
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(bigdecimal)
BuildArch: noarch

%description
Arel is a Relational Algebra for Ruby. It 1) simplifies the generation complex
of SQL queries and it 2) adapts to various RDBMS systems. It is intended to be
a framework framework; that is, you can build your own ORM with it, focusing
on innovative object and collection modeling as opposed to database
compatibility and query generation.


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires:%{name} = %{version}-%{release}

%description doc
Documentation for %{name}

%prep
%setup -q -c -T
%gem_install -n %{SOURCE0}

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
tar xf %{SOURCE1}

# Fix tests according to later upstream commit 0d7b888066b1f319e085c008aeb6c5f3ca05fd8a
sed -i '591s/manager   = Arel::SelectManager.new/manager   = Arel::SelectManager.new Table.engine/' test/test_select_manager.rb
sed -i '606s/manager   = Arel::SelectManager.new/manager   = Arel::SelectManager.new Table.engine/' test/test_select_manager.rb

ruby -Ilib:test -e 'Dir.glob "./test/test_*.rb", &method(:require)'
popd

%files
%dir %{gem_instdir}
%exclude %{gem_instdir}/.*
%{gem_libdir}
%doc %{gem_instdir}/MIT-LICENSE.txt
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_instdir}/History.txt
%doc %{gem_instdir}/README.markdown
%doc %{gem_docdir}


%changelog
* Mon Aug 24 2015 Josef Stribny <jstribny@redhat.com> - 6.0.3-1
- Update to 6.0.3

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Feb 09 2015 Josef Stribny <jstribny@redhat.com> - 6.0.0-1
- Update to 6.0.0

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Apr 11 2014 Josef Stribny <jstribny@redhat.com> - 5.0.0-1
- Update to arel 5.0.0
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.1

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 Josef Stribny <jstribny@redhat.com> - 4.0.0-1
- Update to arel 4.0.0.

* Wed Feb 27 2013 Vít Ondruch <vondruch@redhat.com> - 3.0.2-3
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Vít Ondruch <vondruch@redhat.com> - 3.0.2-1
- Update to Arel 3.0.2.

* Fri Mar 09 2012 Vít Ondruch <vondruch@redhat.com> - 2.0.9-4
- Fix dependency on BigDecimal.

* Thu Jan 19 2012 Vít Ondruch <vondruch@redhat.com> - 2.0.9-3
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Mar 24 2011 Vít Ondruch <vondruch@redhat.com> - 2.0.9-1
- Update to Arel 2.0.9
- Removed unnecessary cleanup

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 28 2011 Vít Ondruch <vondruch@redhat.com> - 2.0.7-1
- Updated to Arel 2.0.7 
- Removed some build dependencies

* Fri Jan 07 2011 Vít Ondruch <vondruch@redhat.com> - 2.0.6-3
- Move all documentation into subpackage

* Fri Jan 07 2011 Vít Ondruch <vondruch@redhat.com> - 2.0.6-2
- Clean buildroot

* Fri Jan 7 2011 Vít Ondruch <vondruch@redhat.com> - 2.0.6-1
- Initial package
