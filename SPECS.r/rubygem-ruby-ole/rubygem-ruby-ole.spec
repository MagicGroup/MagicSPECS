%global gem_name ruby-ole

Summary: Ruby OLE library
Name: rubygem-%{gem_name}
Version: 1.2.11.7
Release: 3%{?dist}
Group: Development/Languages
License: MIT
URL: http://code.google.com/p/ruby-ole
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: rubygems-devel
BuildRequires: rubygem(minitest)
BuildArch: noarch

%description
A library for easy read/write access to OLE compound documents for Ruby.

%package doc
Summary:           Documentation for %{name}
Group:             Documentation
Requires:          %{name} = %{version}-%{release}

%description doc
Documentation for %{name}.


%prep
%setup -q -c -T
%gem_install -n %{SOURCE0}

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gem_dir}
mkdir -p %{buildroot}/%{_bindir}
cp -a .%{_bindir}/* %{buildroot}/%{_bindir}
cp -a .%{gem_dir}/* %{buildroot}%{gem_dir}

# rpmlint cleanup
chmod 755 %{buildroot}%{gem_instdir}/test/test_meta_data.rb


%check
pushd .%{gem_instdir}
# Run the tests using minitest 5.
ruby -rminitest/autorun - << \EOF
  module Kernel
    alias orig_require require
    remove_method :require

    def require path
      orig_require path unless path == 'test/unit'
    end
  end

  module Minitest::Assertions
    alias :assert_raise :assert_raises
  end

  Test = Minitest

  Dir.glob "./test/**/test_*.rb", &method(:require)
EOF
popd

%files
%{_bindir}/oletool
%dir %{gem_instdir}
%doc %{gem_instdir}/README
%doc %{gem_instdir}/COPYING
%doc %{gem_instdir}/ChangeLog
%{gem_libdir}
%{gem_instdir}/bin
%exclude %{gem_cache}
%{gem_spec}


%files doc
%{gem_instdir}/test
%{gem_instdir}/Rakefile
%doc %{gem_docdir}
%{gem_instdir}/*.gemspec


%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.2.11.7-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.11.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jul 15 2014 Vít Ondruch <vondruch@redhat.com> - 1.2.11.7-1
Update to ruby-ole 1.2.11.7.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.11.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.11.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 18 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 1.2.11.2-5
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.11.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.11.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Feb 03 2012 Vít Ondruch <vondruch@redhat.com> - 1.2.11.2-2
- Rebuilt for Ruby 1.9.3.

* Sun Jan 08 2012 Michael Stahnke <mastahnke@gmail.com> - 1.2.11.2-1
- Bump to 1.2.11.2 and fix bug 715865

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Oct 25 2010 Michael Stahnke <stahnma@fedoraproject.org> - 1.2.11.1-1
- License changed to MIT per upstream comments

* Thu Sep 16 2010 Michael Stahnke <stahnma@fedoraproject.org> - 1.2.10.1-1
- Initial package
