# Generated from execjs-1.4.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name execjs

Summary: Run JavaScript code from Ruby
Name: rubygem-%{gem_name}
Version: 2.2.0
Release: 2%{?dist}
Group: Development/Languages
# Public Domain: %%{gem_libdir}/execjs/support/json2.js
License: MIT and Public Domain
URL: https://github.com/sstephenson/execjs
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone https://github.com/sstephenson/execjs.git && cd execjs
# git checkout v2.2.0 && tar czf execjs-2.2.0-tests.tgz test/
Source1: %{gem_name}-%{version}-tests.tgz
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(therubyracer)
BuildArch: noarch

%description
ExecJS lets you run JavaScript code from Ruby. It automatically picks the
best runtime available to evaluate your JavaScript program, then returns
the result to you as a Ruby object.

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

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
tar xzf %{SOURCE1}
# disable test that needs internet connection
sed -i '/def test_coffeescript/,/^  end$/ s/^/#/' test/test_execjs.rb
export LANG=en_US.utf8
ruby -Ilib -e 'Dir.glob "./test/**/test_*.rb", &method(:require)'
popd

%files
%dir %{gem_instdir}
%doc %{gem_instdir}/LICENSE
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 23 2014 Vít Ondruch <vondruch@redhat.com> - 2.2.0-1
- Update to ExecJS 2.2.0.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 07 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 1.4.0-5
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jul 12 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.4.0-2
- Removed the duplicated "git checkout" in comment.
- BR: rubygem(therubyracer) for tests, don't use deprecated js.

* Wed Jun 13 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.4.0-1
- Initial package
