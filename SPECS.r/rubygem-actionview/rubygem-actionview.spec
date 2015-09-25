%global gem_name actionview
%global bootstrap 0

Name: rubygem-%{gem_name}
Version: 4.2.4
Release: 3%{?dist}
Summary: Rendering framework putting the V in MVC (part of Rails)
Group: Development/Languages
License: MIT
URL: http://www.rubyonrails.org
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone http://github.com/rails/rails.git
# cd rails/actionview/
# git checkout v4.2.4
# tar czvf actionview-4.2.4-tests.tgz test/
Source1: %{gem_name}-%{version}-tests.tgz
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
%if 0%{bootstrap} < 1
BuildRequires: rubygem(activesupport) = %{version}
BuildRequires: rubygem(activerecord) = %{version}
BuildRequires: rubygem(actionpack) = %{version}
BuildRequires: rubygem(railties) = %{version}
BuildRequires: rubygem(sqlite3)
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(mocha) >= 0.9.8
%endif
BuildArch: noarch

%description
Simple, battle-tested conventions and helpers for building web pages.


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

%if 0%{bootstrap} < 1
%check
pushd .%{gem_instdir}

tar xzvf %{SOURCE1} -C .

# This requires rails git structure and only requires bundler in the end
sed -i "s|require File.expand_path('../../../load_paths', __FILE__)||" ./test/abstract_unit.rb
sed -i '16,18d' ./test/active_record_unit.rb

# Run separately as we need to avoid superclass mismatch errors
ruby -Ilib:test -e "Dir.glob('./test/{actionpack,activerecord,lib}/*_test.rb').each {|t| require t}"
ruby -Ilib:test -e "Dir.glob('./test/template/*_test.rb').each {|t| require t}"

popd
%endif

%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}
%doc %{gem_instdir}/MIT-LICENSE

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.rdoc
%doc %{gem_instdir}/CHANGELOG.md

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 4.2.4-3
- 为 Magic 3.0 重建

* Wed Aug 26 2015 Josef Stribny <jstribny@redhat.com> - 4.2.4-2
- Enable tests

* Wed Aug 26 2015 Josef Stribny <jstribny@redhat.com> - 4.2.4-1
- Update to actionview 4.2.4

* Wed Jul 01 2015 Josef Stribny <jstribny@redhat.com> - 4.2.3-2
- Enable tests

* Tue Jun 30 2015 Josef Stribny <jstribny@redhat.com> - 4.2.3-1
- Update to actionview 4.2.3

* Tue Jun 23 2015 Josef Stribny <jstribny@redhat.com> - 4.2.2-2
- Run tests

* Mon Jun 22 2015 Josef Stribny <jstribny@redhat.com> - 4.2.2-1
- Update to actionview 4.2.2

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Mar 20 2015 Josef Stribny <jstribny@redhat.com> - 4.2.1-2
- Run tests

* Fri Mar 20 2015 Josef Stribny <jstribny@redhat.com> - 4.2.1-1
- Update to actionview 4.2.1

* Fri Feb 13 2015 Josef Stribny <jstribny@redhat.com> - 4.2.0-2
- Run tests

* Mon Feb 09 2015 Josef Stribny <jstribny@redhat.com> - 4.2.0-1
- Update to actionview 4.2.0

* Mon Aug 25 2014 Josef Stribny <jstribny@redhat.com> - 4.1.5-1
- Update to actionview 4.1.5

* Fri Jul 04 2014 Josef Stribny <jstribny@redhat.com> - 4.1.4-1
- Update to actionview 4.1.4

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 22 2014 Josef Stribny <jstribny@redhat.com> - 4.1.1-1
- Update to ActionView 4.1.1

* Tue Apr 15 2014 Josef Stribny <jstribny@redhat.com> - 4.1.0-2
- Unpack test suite in %%check
- Adjust tests to run with all dependencies

* Thu Apr 10 2014 Josef Stribny <jstribny@redhat.com> - 4.1.0-1
- Initial package
