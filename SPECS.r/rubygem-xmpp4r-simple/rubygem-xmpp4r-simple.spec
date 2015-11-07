%global gem_name xmpp4r-simple

Summary: A simplified Jabber client library
Name: rubygem-%{gem_name}
Version: 0.8.8
Release: 13%{?dist}
Group: Development/Languages
License: GPLv2+
URL: http://xmpp4r-simple.rubyforge.org/
Source0: http://gems.rubyforge.org/gems/%{gem_name}-%{version}.gem
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: ruby(rubygems)
Requires: ruby(release)
Requires: rubygem(xmpp4r)
BuildRequires: rubygems-devel
#BuildRequires: rubygem(rake)
#BuildRequires: rubygem(rcov)
#BuildRequires: rubygem(xmpp4r)
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
Jabber::Simple takes the strong foundation laid by xmpp4r and hides the
relatively high complexity of maintaining a simple instant messenger bot in
Ruby.

%package    doc
Summary:    Documentation for %{name} 
Group:      Documentation
Requires:   %{name} = %{version}-%{release}

%description    doc
This package contains documentation and examples for %{name}.

%prep

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gem_dir}
%gem_install -n %{SOURCE0} -d %{buildroot}%{gem_dir}

%clean
rm -rf %{buildroot}

%if 0
# The test cases require a running XMPP server
%check
pushd %{buildroot}%{gem_instdir}/test
ruby test_xmpp4r_simple.rb 
popd
%endif

%files
%defattr(-, root, root, -)
%dir %{gem_instdir}/
%doc %{gem_instdir}/README
%doc %{gem_instdir}/COPYING
%doc %{gem_instdir}/CHANGELOG
%{gem_libdir}/
%{gem_cache}
%{gem_spec}

%files doc
%defattr(-, root, root, -)
%{gem_docdir}
%{gem_instdir}/test

%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 0.8.8-13
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.8.8-12
- 为 Magic 3.0 重建

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.8-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.8-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 18 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.8.8-9
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Feb 08 2012 Vít Ondruch <vondruch@redhat.com> - 0.8.8-6
- Fixed broken dependencies.

* Thu Feb 02 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.8.8-5
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Apr 09 2010 Mark Chappell <tremble@fedoraproject.org> - 0.8.8-2
- Tidy up macro usage
- Remove duplicate file entries
- Clean up redundant (Build)Require information

* Tue Mar 16 2010 Mark Chappell <tremble@fedoraproject.org> - 0.8.8-1
- Initial package
