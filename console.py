#!/usr/bin/python3
"""airbnb console"""
import cmd
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import models


class HBNBCommand(cmd.Cmd):
    """
    defines class HBNBCommand
    """
    prompt = "(hbnb)"  # Set your custom prompt here
    classes = [
            'BaseModel', 'Amenity', 'City', 'Place', 'Review', 'State', 'User']
  def emptyline(self):
        """Does nothing when finding empty line"""
        pass
    
   def do_EOF(self, line):
        """sees exit of file"""
        return True
     
   def do_quit(self, arg):
        """the command to exit program"""
        return True
     
    def do_create(self, args):
        """creates chances"""
        if args:
            if args in self.classes:
                # class_obj = getattr(base_model, args)
                dummy_instance = eval(args)()
                dummy_instance.save()
                print(dummy_instance.id)
            else:
                print("** class doesn't exist **")
        else:
            print("** class name missing **")

   
    def do_destroy(self, line):
        """removes instance based on class name and id"""
        args = line.split()

        if not args:
            print("** class name missing **")
            return

        class_name = args[0]

        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        instance_id = args[1]
        key = class_name + "." + instance_id

        if key in models.storage.all():
            del models.storage.all()[key]
            models.storage.save()
        else:
            print("** no instance found **")

     def do_show(self, line):
        """Prints str rep of instance"""
        args = line.split()

        if not args:
            print("** class name missing **")
            return

        class_name = args[0]

        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        instance_id = args[1]
        key = class_name + "." + instance_id

        if key in models.storage.all():
            print(models.storage.all()[key])
        else:
            print("** no instance found **")

    def do_count(self, line):
        """tracks number of instances of class"""
        if line in self.classes:
            objects = models.storage.all()
            class_instances = [
                instance for instance in objects.values()
                if type(instance).__name__ == line]
            count = len(class_instances)
            print(count)
        else:
            print("** class doesn't exist **")

    def custom_split(self, line):
        """splits classname and id"""
        args = []
        current_arg = ""
        inside_quotes = False

        for char in line:
            if char == '"':
                inside_quotes = not inside_quotes
            elif char == ' ' and not inside_quotes:
                if current_arg:
                    args.append(current_arg)
                    current_arg = ""
                continue

            current_arg += char

        if current_arg:
            args.append(current_arg)

        return args
      
  def do_all(self, line):
        """Prints str rep of all instances"""
        if line in self.classes:
            objects = models.storage.all()
            class_instances = [
                str(instance) for instance in objects.values()
                if type(instance).__name__ == line]
            print(class_instances)
        elif not line:
            objects = models.storage.all()
            all_instances = [str(instance) for instance in objects.values()]
            print(all_instances)
        else:
            print("** class doesn't exist **")
        
    def do_update(self, line):
        """updates instance based on class name"""
        args = self.custom_split(line)

        if not args:
            print("** class name missing **")
            return

        class_name = args[0]

        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        instance_id = args[1]
        key = class_name + "." + instance_id

        if key not in models.storage.all():
            print("** no instance found **")
            return

        if len(args) < 3:
            print("** attribute name missing **")
            return

        if len(args) < 4:
            print("** value missing **")
            return

        attribute_name = args[2]
        attribute_value = args[3]
        instance = models.storage.all()[key]

        try:
            attribute_value = eval(attribute_value)
        except (NameError, SyntaxError):
            pass

        setattr(instance, attribute_name, attribute_value)
        models.storage.save()

    def default(self, line):
        """automatic command handler method"""
        if line.endswith(".all()"):
            class_name = line[:-6]
            self.do_all(class_name)
        elif line.endswith(".count()"):
            class_name = line[:-8]
            self.do_count(class_name)
        elif ".show" in line:
            for class_name in self.classes:
                if line.startswith(
                        f"{class_name}.show(") and line.endswith(")"):
                    start_index = line.find("(")
                    end_index = line.find(")")
                    instance_id = line[start_index + 2: end_index - 1]
                    line = "{} {}".format(class_name, instance_id)
                    self.do_show(line)
                    return
        elif ".destroy" in line:
            for class_name in self.classes:
                if line.startswith(
                        f"{class_name}.destroy(") and line.endswith(")"):
                    start_index = line.find("(")
                    end_index = line.find(")")
                    instance_id = line[start_index + 2: end_index - 1]
                    line = "{} {}".format(class_name, instance_id)
                    self.do_destroy(line)
                    return
        elif ".update" in line:
            for class_name in self.classes:
                if line.startswith(
                        f"{class_name}.update(") and line.endswith(")"):
                    start_index = line.find("(")
                    end_index = line.find(")")
                    params = line[start_index + 1: end_index].split(", ")
                    if len(params) >= 3:
                        inst_id = params[0][1:-1]
                        attr_name = params[1][1:-1]
                        attr_val = params[2][1:-1]
                        line = f"{class_name} {inst_id} {attr_name} {attr_val}"
                        self.do_update(line)
                        return
                    else:
                        print("*** Missing parameters for update ***")
                        return
        else:
            print("*** Unknown syntax: {}".format(line))
          
if __name__ == '__main__':
    HBNBCommand().cmdloop()
