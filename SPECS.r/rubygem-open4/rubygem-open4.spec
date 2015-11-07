%global gem_name open4

Summary: Manage child processes and their IO handles easily
Name: rubygem-%{gem_name}
Version: 1.3.4
Release: 4%{?dist}
Group: Development/Languages
License: BSD or Ruby
URL: http://github.com/ahoward/open4/
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: rubygems-devel
BuildRequires: rubygem(minitest)
BuildArch: noarch

%description
Open child process with handles on pid, stdin, stdout, and stderr.
Manage child processes and their IO handles easily.

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
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

# Fix rpmlint warning.
sed -i '/#!.*env ruby/d' %{buildroot}%{gem_instdir}/samples/jesse-caldwell.rb

%check
pushd .%{gem_instdir}
ruby -Ilib:test/lib -e 'Dir.glob "./test/**/*_test.rb", &method(:require)'
popd

%files
%dir %{gem_instdir}
%{gem_libdir}
%doc %{gem_instdir}/LICENSE
%doc %{gem_instdir}/README
%doc %{gem_instdir}/README.erb
%exclude %{gem_cache}
%{gem_spec}

%files doc
%{gem_instdir}/rakefile
%{gem_instdir}/samples
%{gem_instdir}/test
%{gem_instdir}/white_box
%{gem_instdir}/%{gem_name}.gemspec
%doc %{gem_docdir}


%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.3.4-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.3.4-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jul 16 2014 Vít Ondruch <vondruch@redhat.com> - 1.3.4-1
- Update to popen4 1.3.4.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 07 2013 Vít Ondruch <vondruch@redhat.com> - 1.3.0-5
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 07 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.3.0-2
- Fixed the license after clarification with the author.

* Tue Jan 24 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.3.0-1
- Rebuilt for Ruby 1.9.3.
- Updated to 1.3.0 version.
- Introduced %%check section for running tests.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Oct 13 2010 Michal Fojtik <mfojtik@redhat.com> - 1.0.1-1
- Initial package
