import { ReactNode, useState } from "react";

import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

import { createChallenge } from "@/services/challenge";

interface Props {
  children: ReactNode;
  onCreated?: () => void;
}

export default function CreateChallengeDialog({
  children,
  onCreated,
}: Props) {
  const [open, setOpen] = useState(false);

  const [form, setForm] = useState({
    name: "",
    description: "",
    goal: 3,
    category: "Estudos",
    type_challenge: "STREAK",
    mode_challenge: "SOLO",
    visibility: false,
    start_date: "",
    end_date: "",
    max_participants: 1
  });

  function setField(field: string, value: any) {
    setForm((prev) => ({
      ...prev,
      [field]: value,
    }));
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();

    try {
      await createChallenge(form);

      setOpen(false);

      setForm({
        name: "",
        description: "",
        goal: 3,
        category: "Estudos",
        type_challenge: "STREAK",
        mode_challenge: "SOLO",
        visibility: false,
        start_date: "",
        end_date: "",
        max_participants:1,
      });

      onCreated?.();
    } catch (err) {
      console.error(err);
    }
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>{children}</DialogTrigger>

      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle>Criar desafio</DialogTitle>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <Label>Nome</Label>

            <Input
              value={form.name}
              onChange={(e) => setField("name", e.target.value)}
            />
          </div>

          <div>
            <Label>Descrição</Label>

            <Input
              value={form.description}
              onChange={(e) => setField("description", e.target.value)}
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label>Categoria</Label>

              <select
                className="w-full rounded-md border p-2"
                value={form.category}
                onChange={(e) => setField("category", e.target.value)}
              >
                <option>Estudos</option>
                <option>Leitura</option>
                <option>Exercicio</option>
                <option>Idiomas</option>
                <option>Saude</option>
              </select>
            </div>

            <div>
              <Label>Tipo</Label>

              <select
                className="w-full rounded-md border p-2"
                value={form.type_challenge}
                onChange={(e) =>
                  setField("type_challenge", e.target.value)
                }
              >
                <option value="STREAK">STREAK</option>
                <option value="TIME">TIME</option>
                <option value="AMOUNT">AMOUNT</option>
              </select>
            </div>
          </div>

          <div>
            <Label>Modo</Label>

            <select
              className="w-full rounded-md border p-2"
              value={form.mode_challenge}
              onChange={(e) =>
                setField("mode_challenge", e.target.value)
              }
            >
              <option value="SOLO">SOLO</option>
              <option value="GROUP">GROUP</option>
              <option value="COMPETITION">COMPETITION</option>
            </select>
          </div>

          <div>
            <Label>Meta</Label>

            <Input
              type="number"
              value={form.goal}
              onChange={(e) =>
                setField("goal", Number(e.target.value))
              }
            />
          </div>

          <div>
            <Label>Número máximo de participantes</Label>

            <Input
              type="number"
              value={form.max_participants}
              onChange={(e) =>
                setField("max_participants", Number(e.target.value))
              }
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label>Data inicial</Label>

              <Input
                type="date"
                value={form.start_date}
                onChange={(e) =>
                  setField("start_date", e.target.value)
                }
              />
            </div>

            <div>
              <Label>Data final</Label>

              <Input
                type="date"
                value={form.end_date}
                onChange={(e) =>
                  setField("end_date", e.target.value)
                }
              />
            </div>
          </div>

          <div className="flex items-center gap-2">
            <input
              id="visibility"
              type="checkbox"
              checked={form.visibility}
              onChange={(e) =>
                setField("visibility", e.target.checked)
              }
            />

            <Label htmlFor="visibility">Público</Label>
          </div>

          <div className="flex justify-end gap-2">
            <Button
              type="button"
              variant="secondary"
              onClick={() => setOpen(false)}
            >
              Cancelar
            </Button>

            <Button type="submit">
              Criar desafio
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
}